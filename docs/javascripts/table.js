class SassyTables {
    static filterColumn = 'mandatory';
    static controlHtml = '<button type="button" class="pon-pm-icon"></button>';

    constructor() {
        this.processTables();
    }

    processTables() {
        const tables = document.querySelectorAll('table');

        tables.forEach(table => this.processTable(table));
    }

    processTable(table) {
        const headerRow = table.querySelector('thead tr');

        if (!headerRow) return;

        const columnIndex = this.findColumnIndexWithText(headerRow, SassyTables.filterColumn);

        if (columnIndex === -1) return;

        const tableRows = this.findEmptyColumnRows(table, columnIndex);

        if (tableRows.length > 0) {
            tableRows.forEach(tableRow => {
                tableRow.style.display = 'none';
            });

            this.addToggleControl(table, tableRows);
        }
    }

    findColumnIndexWithText(tableRow, filterText) {
        const headings = tableRow.querySelectorAll('th, td');

        for (let i = 0; i < headings.length; i++) {
            if (headings[i].textContent.trim().toLowerCase() === filterText.toLowerCase()) {
                return i + 1;
            }
        }

        return -1;
    }

    findEmptyColumnRows(table, columnIndex) {
        const tableRows = table.querySelectorAll('tbody tr');

        const emptyRows = [];

        tableRows.forEach(tableRow => {
            const cell = tableRow.querySelector(`td:nth-child(${columnIndex})`);

            if (cell && !cell.childElementCount && !cell.textContent.trim().length) {
                emptyRows.push(tableRow);
            }
        });

        return emptyRows;
    }

    createToggleControl() {
        const template = document.createElement('template');

        template.innerHTML = SassyTables.controlHtml;

        return template.content.firstElementChild;

    }

    addToggleControl(table, hiddenRows) {
        const toggleControl = this.createToggleControl();

        toggleControl.addEventListener('transitionend', (e) => {
          e.preventDefault;
            hiddenRows.forEach(row => {
                row.style.display = e.target.classList.contains('pon-pm-icon--active') ? '' : 'none';
            });
        });

        toggleControl.addEventListener('click', (e) => {
            e.preventDefault;
            toggleControl.classList.toggle('pon-pm-icon--active');
        });

        table.insertAdjacentElement('afterend', toggleControl);
    }
}

document.addEventListener('DOMContentLoaded', () => {
  new SassyTables();
});
