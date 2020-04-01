const gen_datatables_config = (overwrites) => {
  const column_selector = (idx, data, node) => {
    // https://datatables.net/forums/discussion/42192/exporting-data-with-buttons-and-responsive-extensions-controlled-by-column-visibility
    // When the colvis/responsive plugin hides a column this might be done in one of 2 ways:
    // By adding the noVis class or by physically detaching the DOM element from the table
    if ($(node).hasClass('noVis')) {
      return false;
    }
    const table = $(node).closest('table');
    return table.length === 0 ? false : table.DataTable().column(idx).visible();
  };

  function strip_tags(data, row, column, node)
  {
    return $.trim($("<div/>").html(data).text().replace(/( *\n *)+/g, '\n').replace(/ +/g, ' '));
  }

  function strip_tags_and_newlines(data, row, column, node)
  {
    return strip_tags(data, row, column, node).replace('\n', ', ');
  }

  function strip_tags_and_checkmark(data, row, column, node)
  {
    // TODO: fix checkmark rendering so that this is not required
    data = data.replace('<span class="qualified">✔</span>', '');
    data = data.replace('<span class="not-qualified">✘</span>', '');
    data = data.replace('<span class="maybe-qualified">?</span>', '');
    return strip_tags(data, row, column, node);
  }

  return Object.assign({
    dom: 'Bfrtipl',
    responsive: true,
    colReorder: true,
    deferRender: true,
    createdRow: (row) => {
      $(row).find('[data-toggle="popover"]').popover();
    },
    buttons: [
      {
        extend: 'colvis',
        columns: ':gt(0)'
      },
      {
        extend: 'copy',
        exportOptions: {
          columns: column_selector,
          format: { body: strip_tags_and_newlines }
        }
      },
      {
        extend: 'excel',
        exportOptions: {
          columns: column_selector,
          format: { body: strip_tags_and_checkmark }
        }
      },
      {
        extend: 'pdf',
        exportOptions: {
          columns: column_selector,
          format: { body: strip_tags_and_checkmark }
        },
       },
       {
        extend: 'print',
        exportOptions: {
          columns: column_selector,
          format: { body: strip_tags }
        }
       },
    ],
    "language": {
      "url": datatables_locale_url,
    },
    "fnRowCallback" : function(nRow, aData, iDisplayIndex){
      $("td:first", nRow).html(iDisplayIndex +1);
      return nRow;
    },
    "pageLength": 50,
    "lengthMenu": [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]],
  }, overwrites);
};
