(() => {
  const CONFIG = {
    columnText: 'mandatory',
    controlHtml: '<button type="button" class="pon-pm-icon"></button>',
    activeClass: 'pon-pm-icon--active'
  };

  const animateRow = (row, show) => {
    if (show) {
      row.style.display = '';
      row.animate([
        { opacity: 0, transform: 'translateY(-5px)' },
        { opacity: 1, transform: 'translateY(0)' }
      ], { duration: 250, easing: 'ease-out' });
    } else {
      const anim = row.animate([
        { opacity: 1 },
        { opacity: 0, transform: 'translateY(-5px)' }
      ], { duration: 200, easing: 'ease-in' });
      anim.onfinish = () => (row.style.display = 'none');
    }
  };

  const processTable = (table) => {
    if (table.dataset.toggleInitialized) return;

    const headers = [...table.querySelectorAll('thead th, thead td')];
    const colIdx = headers.findIndex(h => h.textContent.trim().toLowerCase() === CONFIG.columnText) + 1;

    if (colIdx === 0) return;

    const rows = [...table.querySelectorAll('tbody tr')].filter(row => {
      const cell = row.querySelector(`td:nth-child(${colIdx})`);
      return cell && !cell.childElementCount && !cell.textContent.trim().length;
    });

    if (rows.length === 0) return;

    rows.forEach(row => (row.style.display = 'none'));

    const template = document.createElement('template');
    template.innerHTML = CONFIG.controlHtml;
    const btn = template.content.firstElementChild;

    const wrapper = document.createElement('div');
    wrapper.className = 'table-toggle-bridge';
    wrapper.appendChild(btn);

    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const isActive = btn.classList.toggle(CONFIG.activeClass);
      rows.forEach(row => animateRow(row, isActive));
    });

    table.insertAdjacentElement('afterend', wrapper);
    table.dataset.toggleInitialized = "true";
  };

  const load = () => document.querySelectorAll('table').forEach(processTable);

  if (typeof app !== "undefined") {
    app.document$.subscribe(load);
  } else {
    document.readyState === 'loading'
      ? document.addEventListener('DOMContentLoaded', load)
      : load();
  }
})();
