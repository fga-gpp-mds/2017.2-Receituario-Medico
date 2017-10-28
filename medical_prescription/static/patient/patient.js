  $(document).ready(function($) {

    //Creating mascara for form fields
    var $date_of_birth = $("#id_date_of_birth");
    $date_of_birth.mask('00/00/0000');

    function limpa_formulário_cep() {
      // Cleans cep form values.
      $("#rua").val("");
      $("#bairro").val("");
      $("#cidade").val("");
      $("#id_UF").val("");
    }

    //When the cep field loses focus.
    $("#id_CEP").blur(function() {

      //New variable "cep" with digits only.
      var cep = $(this).val().replace(/\D/g, '');


      if (cep != "") {

        //Regular expression to validate the CEP.
        var validacep = /^[0-9]{8}$/;

        // Validate the format of the CEP.
        if (validacep.test(cep)) {

          // Fill fields while querying API.
          $("#id_complement").val("Buscando...");
          $("#id_neighborhood").val("Buscando...");
          $("#id_city").val("Buscando...");
          $("#id_UF").val("Buscando...");

          // Check the webservice viacep.com.br/
          $.getJSON("https://viacep.com.br/ws/" + cep + "/json/?callback=?", function(dados) {

            if (!("erro" in dados)) {
              // Refreshes fields with query values.
              $("#id_complement").val(dados.logradouro);
              $("#id_neighborhood").val(dados.bairro);
              $("#id_city").val(dados.localidade);
              $("#id_UF").val(dados.uf);
            } //end if.
            else {
              limpa_formulário_cep();
              alert("CEP não encontrado.");
            }
          });
        } //end if.
        else {
          limpa_formulário_cep();
          alert("Formato de CEP inválido.");
        }
      } //end if.
      else {
        // no value, clean form.
        limpa_formulário_cep();
      }
    });
  });
