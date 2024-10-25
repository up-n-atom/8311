window.addEventListener("pageshow", () => {
  try {
    const selectElement = document.querySelector('select[isp]');
    selectElement.value = '#';
  } catch (e) {}
});

document.addEventListener('DOMContentLoaded', () => {
  try {
    const selectElement = document.querySelector('select[isp]');
    selectElement.onchange = (event) => {
      const category = event.target.value;
      if (category && category !== '#') {
        window.location.href = location.origin + '/category/' + category;
      }
    };
  } catch (e) {}
});
