(async () => {
  const svgPanZoom = (await import('https://cdn.jsdelivr.net/npm/svg-pan-zoom@3.6.1/+esm')).default;

  const shadowRoots = new WeakMap();
  const originalAttachShadow = Element.prototype.attachShadow;
  Element.prototype.attachShadow = function(init) {
    const shadow = originalAttachShadow.call(this, init);
    shadowRoots.set(this, shadow);
    return shadow;
  };

  const getPZConfig = (isInline, controller) => ({
    zoomEnabled: true,
    controlIconsEnabled: true,
    fit: true,
    center: true,
    minZoom: 0.1,
    maxZoom: 10,
    mouseWheelZoomEnabled: !isInline,
    customEventsHandler: {
      haltEventListeners: ['touchstart', 'touchend', 'touchmove', 'touchleave', 'touchcancel'],
      init({ instance, svgElement }) {
        const { signal } = controller;

        this.onResize = () => {
          instance.resize();
          instance.center();
          if (!isInline) instance.fit();
        };

        const onGrab = () => (svgElement.style.cursor = 'grabbing');
        const onRelease = () => (svgElement.style.cursor = 'grab');

        window.addEventListener('resize', this.onResize, { signal });
        window.addEventListener('mouseup', onRelease, { signal });
        svgElement.addEventListener('mousedown', onGrab, { signal });

        instance.resize();
        instance.center();
      },
      destroy() {
        controller.abort();
      }
    }
  });

  const initDiagram = (host) => {
    if (host.dataset.pzInitialized) return;
    const shadow = shadowRoots.get(host);

    const observer = new ResizeObserver(() => {
      const svg = shadow?.querySelector('svg');
      if (!svg || svg.getBBox().width === 0) return;

      observer.disconnect();
      host.dataset.pzInitialized = "true";
      renderPanZoom(host, svg);
    });

    observer.observe(host);
  };

  const renderPanZoom = (host, svg) => {
    const shadow = shadowRoots.get(host);
    const inlineController = new AbortController();

    const vb = svg.getAttribute('viewBox')?.split(/\s+/).map(Number);
    if (vb?.length === 4) {
      const [,, vBWidth, vBHeight] = vb;
      host.style.height = 'auto';
      host.style.aspectRatio = `${vBWidth} / ${vBHeight}`;
      host.style.maxHeight = '75vh';
      host.style.width = '100%';
      host.style.overflow = 'hidden';
      host.style.position = 'relative';
    }
    if (shadow.firstElementChild) shadow.firstElementChild.style.overflow = 'hidden';
    svg.style.cssText = 'max-width:none; width:100%; height:100%; cursor:grab;';
    ['width', 'height'].forEach(attr => svg.removeAttribute(attr));

    const inlinePZ = svgPanZoom(svg, getPZConfig(true, inlineController));

    let isDragging = false;
    let startX = 0;
    let startY = 0;
    const dragThreshold = 5;

    svg.addEventListener('mousedown', (e) => {
      isDragging = false;
      startX = e.clientX;
      startY = e.clientY;
    }, { signal: inlineController.signal });

    svg.addEventListener('mousemove', (e) => {
      if (Math.abs(e.clientX - startX) > dragThreshold ||
          Math.abs(e.clientY - startY) > dragThreshold) {
        isDragging = true;
      }
    }, { signal: inlineController.signal });

    svg.addEventListener('click', (e) => {
      if (isDragging) {
        e.stopImmediatePropagation();
        return;
      }

      if (e.target.closest('.svg-pan-zoom-control')) return;

      const expandedSvg = svg.cloneNode(true);
      const viewport = expandedSvg.querySelector('.svg-pan-zoom_viewport');
      if (viewport) {
        while (viewport.firstChild) expandedSvg.appendChild(viewport.firstChild);
        viewport.remove();
      }
      expandedSvg.querySelector('.svg-pan-zoom-control')?.remove();
      expandedSvg.style.cssText = 'display:block; width:100%; height:100%;';

      const lb = GLightbox({
        elements: [{ content: `<div id="lb-container" style="width:90vw; height:80vh;"></div>` }],
        width: '90vw', height: '80vh', touchNavigation: false, draggable: false,
      });

      lb.on('open', () => {
        const container = document.getElementById('lb-container');
        if (!container) return;
        container.appendChild(expandedSvg);
        const lbController = new AbortController();
        const expandedPZ = svgPanZoom(expandedSvg, getPZConfig(false, lbController));
        lb.on('close', () => {
          expandedPZ.destroy();
          expandedSvg.remove();
        }, { once: true });
      });

      lb.open();
    }, { signal: inlineController.signal });
  };

  const load = () => {
    document.querySelectorAll('.mermaid').forEach(initDiagram);
  };

  if (typeof app !== "undefined") {
    app.document$.subscribe(load);
  } else {
    new MutationObserver(muts => {
      muts.forEach(m => m.addedNodes.forEach(n => {
        if (n.nodeType === 1 && n.classList.contains('mermaid')) initDiagram(n);
      }));
    }).observe(document.body, { childList: true, subtree: true });
  }
})();
