// Parche de postprocesado para el programa SISTEDES 2026.
// Úsalo si prefieres mantener el index.html original: inclúyelo justo antes de </body>.
(() => {
  const PROLE_ROOM = 'Aula Institucional / PROLE';
  const ROOM_LINKS = {
    'Aula 1.2': 'https://cvnet.cpd.ua.es/FichaAula/es/Aula/Ver/0101P2007',
    'Aula 1.1': 'https://cvnet.cpd.ua.es/FichaAula/es/Aula/Ver/0101P1003',
    'Aula Rafael Altamira': 'https://cvnet.cpd.ua.es/FichaAula/es/Aula/Ver/0101PB005',
    'Aula 2.2': 'https://cvnet.cpd.ua.es/FichaAula/es/Aula/Ver/0101P2001'
  };
  const TRACK_IDS = ['AI4SE', 'ASV', 'ICD', 'ISDM', 'ISGD', 'MCPS', 'METODOS', 'QUANTUM'];
  const app = document.getElementById('sprog-app') || document.body;

  function isTrackView() {
    const hash = decodeURIComponent(location.hash || '').replace(/^#/, '').replace(/^track-/, '');
    return TRACK_IDS.includes(hash);
  }

  function stripLinksInTrackView() {
    if (!isTrackView()) return;
    app.querySelectorAll('a').forEach(anchor => {
      const text = anchor.textContent || '';
      if (ROOM_LINKS[text.trim()]) return;
      if (anchor.matches('[data-sprog-home], .sprog-button')) return;
      anchor.replaceWith(document.createTextNode(text));
    });
  }

  function removeVestibuloHashLinks() {
    app.querySelectorAll('a[href="#"]').forEach(anchor => {
      if ((anchor.textContent || '').trim().toLowerCase() === 'vestíbulo sede') {
        anchor.replaceWith(document.createTextNode('Vestíbulo sede'));
      }
    });
  }

  function removeProleCells() {
    app.querySelectorAll('.sprog-slot--prole').forEach(element => {
      const cell = element.closest('td, th, li, article, section, div');
      if (cell) cell.remove();
    });

    app.querySelectorAll('table').forEach(table => {
      const rows = [...table.rows];
      if (!rows.length) return;
      const proleIndexes = [];
      [...rows[0].cells].forEach((cell, index) => {
        const text = (cell.textContent || '').trim();
        if (text.includes(PROLE_ROOM) || /\bPROLE\b/i.test(text)) proleIndexes.push(index);
      });
      if (!proleIndexes.length) return;
      rows.forEach(row => {
        [...row.cells].forEach((cell, index) => {
          if (proleIndexes.includes(index)) cell.remove();
        });
      });
    });

    app.querySelectorAll('td, th, div, span').forEach(element => {
      const text = (element.textContent || '').trim();
      if (text === PROLE_ROOM || text === 'PROLE') {
        const cell = element.closest('td, th');
        if (cell) cell.remove();
      }
    });
  }

  function linkRoomLabels() {
    const selector = 'th, td, h2, h3, h4, .sprog-room, .sprog-track-meta, .sprog-slot-title';
    app.querySelectorAll(selector).forEach(element => {
      if (element.closest('a, button')) return;
      if (element.children.length > 1) return;
      const text = (element.textContent || '').trim();
      const url = ROOM_LINKS[text];
      if (!url) return;
      element.innerHTML = `<a href="${url}" target="_blank" rel="noopener noreferrer">${text}</a>`;
    });
  }

  function run() {
    removeProleCells();
    removeVestibuloHashLinks();
    stripLinksInTrackView();
    linkRoomLabels();
  }

  let scheduled = false;
  function scheduleRun() {
    if (scheduled) return;
    scheduled = true;
    requestAnimationFrame(() => {
      scheduled = false;
      run();
    });
  }

  run();
  new MutationObserver(scheduleRun).observe(app, { childList: true, subtree: true });
  window.addEventListener('hashchange', scheduleRun);
})();
