$(document).ready(function(){

    var autoupdate = false;

    function date1(){
    $('.date-picker').daterangepicker({
      singleDatePicker: true,
      showDropdowns: true,
      maxDate:moment(),
      autoApply: true,
      autoUpdateInput: autoupdate,
      locale: {
        format: 'DD/MM/YYYY'
      }
    }, function(chosen_date) {
      $('.date-picker').val(chosen_date.format('DD/MM/YYYY'));
    });
      };
    date1();
    
    $('.date-picker-2').daterangepicker({
      singleDatePicker: true,
      showDropdowns: true,
      autoApply: true,
      autoUpdateInput: false,
      locale: {
        format: 'DD/MM/YYYY'
      }
    }, function(chosen_date) {
      $('.date-picker-2').val(chosen_date.format('DD/MM/YYYY'));
    });
    
    $('.date-picker').on('apply.daterangepicker', function(ev, picker) {
        if ($('.date-picker').val().length == 0 ){
        
        autoupdate = true;
        console.log('true');
        date1();
      };
      var departpicker = $('.date-picker').val();
      $('.date-picker-2').daterangepicker({
        
        minDate:departpicker,
        maxDate:moment(),
        singleDatePicker: true,
        showDropdowns: true,
        autoApply: true,
        locale: {
          format: 'DD/MM/YYYY'
        }
      });
      
      var drp = $('.date-picker-2').data('daterangepicker');
      drp.setStartDate(departpicker);
      drp.setEndDate(departpicker);
    });
    
    
    $('#clear').click(function(){
     $('input.form-control').val('');
    });
    
});