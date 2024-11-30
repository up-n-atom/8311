const swiper = new Swiper('.swiper', {
  createElements: true,
  pagination: {
    auto: true,
    clickable: true,
    renderBullet: function (index, className) {
      const step = this.slides[index].hasAttribute('step') ? this.slides[index].getAttribute('step') : index + 1;
      return '<span class="' + className + '">' + step + "</span>";
    },
  },
  navigation: true,
  on: {
    afterInit: function (swiper) {
      const zip = (...arrays) => {
        const length = Math.min(...arrays.map(arr => arr.length));
        return Array.from({ length }, (value, index) => arrays.map((array => array[index])));
      };

      let stepsElement = this.el.nextElementSibling;

      while (!(stepsElement instanceof HTMLOListElement)) {
        stepsElement = stepsElement.nextElementSibling || stepsElement.nextSibling;
      }

      let stepElements = stepsElement.querySelectorAll(':scope > li');

      let steps = this.slides.map((el, i) => el.hasAttribute('step') ? el.getAttribute('step') - 1 : i);

      zip(steps, stepElements).forEach(function (step) {
        ['click', 'mouseover'].forEach((e) => step[1].addEventListener(e, () => swiper.slideTo(step[0])));
      });

      /*this.slides.map((el, i) => el.hasAttribute('step') ? el.getAttribute('step') - 1 : i).forEach(function (index) {
        if (index < stepsElement.children.length && stepsElement.children[index] instanceof HTMLLIElement) {
          ['click', 'mouseover'].forEach(function (e) {
            stepsElement.children[index].addEventListener(e, () => swiper.slideTo(index));
          });
        }
      });*/
    },
  },
});
