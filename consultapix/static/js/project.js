const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

document.addEventListener('click', () => {
  tooltipList.forEach(tooltip => tooltip.hide());
});

const processAllButton = document.getElementById('process-all');

function processAll() {
  if (!confirm('Todas as requisições não processadas serão submetidas. Deseja continuar?')) {
    return;
  }
  const allRows = document.querySelectorAll('tr.requisicao-rows');

  allRows.forEach(row => {
    const tr = row.closest('tr');
    if (tr) {
      const processLink = tr.querySelector('#process-row');
      if (processLink) {
        processLink.click();
      }
    }
  });
}

if (processAllButton) {
  processAllButton.addEventListener('click', processAll);
}
