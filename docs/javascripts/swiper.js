(() => {
  const sync = (s, list) => {
    s.slides.forEach((el, i) => {
      const idx = el.hasAttribute('step') ? Number(el.getAttribute('step')) - 1 : i;
      const li = list.children[idx];
      if (li instanceof HTMLLIElement) {
        li.dataset.slideTo = i;
        li.classList.toggle('step-flash', i === s.activeIndex);
      }
    });
  };

  const load = () => {
    new Swiper('.swiper', {
      createElements: true,
      observer: true,
      observeParents: true,
      pagination: {
        auto: true,
        clickable: true,
        renderBullet: function(i, cls) {
          const step = this.slides[i].getAttribute('step') || (i + 1);
          return `<span class="${cls}">${step}</span>`;
        }
      },
      navigation: true,
      on: {
        init: function(s) {
          let list = s.el.nextElementSibling;
          while (list && !(list instanceof HTMLOListElement)) {
            list = list.nextElementSibling;
          }

          if (!list) return;

          sync(s, list);

          ['click', 'mouseover'].forEach(type => {
            list.addEventListener(type, (e) => {
              const li = e.target.closest('li');
              if (!li?.dataset.slideTo) return;

              const targetIdx = Number(li.dataset.slideTo);
              if (type === 'click' || s.activeIndex !== targetIdx) {
                s.slideTo(targetIdx);
              }
            });
          });

          s.linkedList = list;
          list.dataset.swiperLinked = "true";
        },

        observerUpdate: (s) => s.linkedList && sync(s, s.linkedList),
        slideChange: (s) => s.linkedList && sync(s, s.linkedList)
      }
    });
  };

  document.readyState === 'loading'
    ? document.addEventListener('DOMContentLoaded', load)
    : load();
})();
