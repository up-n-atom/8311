document.addEventListener('DOMContentLoaded', (event) => {
  try {
    const selectElement = document.querySelector('select[isp]');
    selectElement.onchange = (event) => {
      const category = event.target.options[event.target.selectedIndex].value;
      if (category) {
        window.location.href=location.origin+'/category/'+category;
      }
    };
  } catch (e) {}
});
