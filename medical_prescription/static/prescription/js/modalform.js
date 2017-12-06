var modal_show_suggestion = false;

// Create prescription.
$(document).on('click', '.js-create-prescription', function() {
  loadForm(this, "#modal-prescription");
});

$("#modal-prescription").on("submit", ".js-prescription-create-form",{id_modal: "#modal-prescription"} ,saveForm);


// Update prescription.
$(document).on('click', '.js-update-prescription', function() {
  loadForm(this, "#modal-prescription");
});

$(document).on('submit', '.js-prescription-update-form', function() {
  saveForm(this, "#modal-prescription");
});

// Delete prescription.
$(document).on('click', '.js-delete-prescription', function() {
  loadForm(this, "#modal-prescription");
});

$(document).on('submit', '.js-prescription-delete-form', function() {
  saveForm(this, "#modal-prescription");
});

// Show prescription.
$(document).on('click', '.js-show-prescription', function() {
  modal_show_suggestion = false;
  loadForm(this, "#modal-view");
});

// Show suggestion
$(document).on('click', '.js-show-suggestion', function() {
  $("#modal-prescription").modal("hide");
  modal_show_suggestion = true;
  loadForm(this, "#modal-view");
});

$(document).on('click', '.btn-return-modal', function() {
  $("#modal-view").modal("hide");
  if(modal_show_suggestion){
    modal_show_suggestion = false;
    $("#modal-prescription").modal("show");
  }
});

$(document).on('click', '.js-create-copy', function() {
  $("#modal-view").modal("hide");
  loadForm(this, "#modal-prescription");
});

/* Functions */
var modalIsCreated = false;

function loadForm(event, id_modal) {
  var btn = $(event);

  $(id_modal).modal({
    backdrop: 'static',
    keyboard: false
  })

  if (!modalIsCreated) {
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      async: true,
      success: function(data) {
        $(id_modal + " .modal-content").html("");
        $(id_modal).modal("show");
        modalIsCreated = false;
        $(id_modal + " .modal-content").html(data.html_form);
      }
    });
  } else {
    $(id_modal).modal("show");
  }
};

function saveForm(event) {
  var form = $(this);
  $.ajax({
    url: form.attr("action"),
    data: form.serialize(),
    type: form.attr("method"),
    dataType: 'json',
    success: function(data) {
      console.log(data.form_is_valid);
      if (data.form_is_valid) {
        modalIsCreated = false;
        $(event.data.id_modal).modal("hide");
        modal_show_suggestion = false;

        // Get url in button to render prescription in another modal.
        var url_get = $("#save").attr("data-url");
        url_get = url_get.replace('None',data.id_prescription);
        event['data-url'] = url_get;
        loadForm(event, "#modal-view");
      } else {
        $(event.data.id_modal).modal("show");
        $(event.data.id_modal + " .modal-content").html(data.html_form);
      }
    }
  });
  return false;
};
