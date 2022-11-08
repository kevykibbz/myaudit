$(document).on('click','.btn-remove',function()
{
  $(this).parent().hide().find('.loader-container').html(`<div class="loader"><svg class="circular" viewBox="25 25 50 50"><circle class="path" cx="50" cy="50" r="10" fill="none" stroke-width="2" stroke-miterlimit="10"/></svg></div>`);
  return false;                                                
});




$(document).on('click','.button1',function()
{
    $('.owl-dot:nth-child(2)').click();
});

$(document).on('click','.button2',function()
{
    $('.owl-dot:last').click();
});


$(document).on('click','.nextBtn',function()
{
    var class_name=$(this).parents('.section').attr('class').split(' ')[2];
    $(this).parents('.section').hide().next().show();
    $('.hh-grayBox').find('.'+class_name).addClass('completed')
});
$(document).on('click','.prevBtn',function()
{
    var class_name=$(this).parents('.section').attr('class').split(' ')[2];
    $(this).parents('.section').hide().prev().show();
    $('.hh-grayBox').find('.'+class_name).removeClass('completed')
});

$(document).on('click','.finishBtn',function()
{
    var class_name=$(this).parents('.section').attr('class').split(' ')[2];
    $('.hh-grayBox').find('.'+class_name).addClass('completed')
});

 $(document).on('submit','.installationForm',function()
 {
     var el=$(this),
     btn_txt=el.find('button:last').html(),
     form_data=new FormData(this);
     $('.feedback').html('');
     $('.hh-grayBox').find('.order-tracking span').removeClass('error');
     $('.hh-grayBox').find('.order-tracking p').removeClass('perror');
     el.children().find('.is-invalid').removeClass('is-invalid');
     el.parent().find('.load-overlay .loader-container').html(`<div class="innerloader"><svg class="circular" viewBox="25 25 50 50"><circle class="path" cx="50" cy="50" r="10" fill="none" stroke-width="2" stroke-miterlimit="10"/></svg></div>`);
     $.ajax(
     {
         url:el.attr('action'),
         method:el.attr('method'),
         dataType:'json',
         data:form_data,
         contentType:false,
         cache:false,
         processData:false,
         beforeSend:function()
         {
            el.parent().find('.load-overlay').show();
            el.find('button:last').attr('disabled',true).text('Please wait...');
         },
         success:function(callback)
         {
            el.parent().find('.load-overlay').hide();
            el.find('button:last').attr('disabled',false).text('finish');
             if(callback.valid)
             {
                el.parent().find('.load-overlay .loader-container').html('<h6 class="text-success" style="font-size:16px !important;"><i class="fa fa-check-circle"></i> '+callback.message+'</h6>');
                el.find('button:last').attr('disabled',true).html(btn_txt);
                window.location='/';
             }
             else
             {
                var class_name=''
                $.each(callback.userform_errors,function(key,value)
                {
                    el.find("input[aria-label='"+key+"'],select[aria-label='"+key+"']").addClass('is-invalid').parents('.form-group').find('.feedback').addClass('text-danger').html('<i class="fa fa-exclamation-circle"></i> '+value);
                    class_name=$("input[aria-label='"+key+"']").parent().parent().parent().attr('class').split(' ')[2];
                    $('.hh-grayBox').find('.'+class_name+' .is-complete').addClass('error');
                    $('.hh-grayBox').find('.'+class_name+' p').addClass('perror');
                });
                $.each(callback.extendedForm_errors,function(key,value)
                {
                    el.find("input[aria-label='"+key+"'],select[aria-label='"+key+"']").addClass('is-invalid').parents('.form-group').find('.feedback').addClass('text-danger').html('<i class="fa fa-exclamation-circle"></i> '+value);
                    class_name=$("input[aria-label='"+key+"']").parent().parent().parent().attr('class').split(' ')[2];
                    $('.hh-grayBox').find('.'+class_name+' .is-complete').addClass('error');
                    $('.hh-grayBox').find('.'+class_name+' p').addClass('perror');
                });
                $.each(callback.siteconstantform_errors,function(key,value)
                {
                    el.find("input[aria-label='"+key+"'],select[aria-label='"+key+"']").addClass('is-invalid').parents('.form-group').find('.feedback').addClass('text-danger').html('<i class="fa fa-exclamation-circle"></i> '+value);
                    class_name=$("input[aria-label='"+key+"']").parent().parent().parent().attr('class').split(' ')[2];
                    $('.hh-grayBox').find('.'+class_name+' .is-complete').addClass('error');
                    $('.hh-grayBox').find('.'+class_name+' p').addClass('perror');
                });
             }
         },
         error:function(err)
         {
            el.find('button:last').attr('disabled',false).text('finish');
            el.parent().find('.load-overlay .loader-container').html('<span class="text-danger font-weight-bold"><i class="icon-exclamation-circle"></i> '+err.status+' :'+err.statusText+'</span>.');
         }
     });
     return false;
 });