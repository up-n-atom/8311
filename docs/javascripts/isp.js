function changeEventHandler(event) {
  const category = this.options[this.selectedIndex].value;
  if (category) {
    window.location.href = location.origin + '/category/' + category;
  }
}

document.addEventListener('DOMContentLoaded', function() {
  let selectElement = document.querySelector('select[isp]');
  selectElement.value='';
  selectElement.onchange=changeEventHandler;
}, false);

