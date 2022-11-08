let element, endTime,mins, msLeft, time,dt,form_data,myTimeout;
const cookieContainer=document.querySelector('.cookie-container');
const cookieButton=document.querySelector('.cookieBtn');
cookieButton.addEventListener('click',()=>{
    cookieContainer.classList.remove('active');
    localStorage.setItem('cookieSet',true);
});
setTimeout(()=>{
    if(!localStorage.getItem('cookieSet'))
    {
        cookieContainer.classList.add('active');
    }
},5000);

/*proloader*/
function load()
{
  document.querySelector('.placeholder').style.display="none";
  document.querySelector('.main-display').style.display="block";
}
/*insection observer API */
function observerImages()
{
    var images=document.querySelectorAll('[data-src]'),
    imgOpts={},
    observer=new IntersectionObserver((entries,observer)=>
    {
        entries.forEach((entry)=>
        {
            if(!entry.isIntersecting) return;
            const img=entry.target;
            const newUrl=img.getAttribute('data-src');
            img.src=newUrl;
            observer.unobserve(img);
        });
    },imgOpts);
  
    images.forEach((image)=>
    {
      observer.observe(image)
    });
}

function twoDigits(n) 
{
    return (n <= 9 ? '0' + n : n);
}

function countdown(elementName, minutes, seconds) 
{
    dt=new Date();
    form_data=new FormData();
    dt.setMinutes(dt.getMinutes() + minutes);
    endTime =dt.getTime();
    element = document.getElementById(elementName);
    updateTimer();
}

function updateTimer() 
{
  msLeft = endTime - (new Date().getTime());
  if (msLeft < 1000) 
  {
        var  id=JSON.parse(document.getElementById('userid').textContent);
        form_data.append('test_passed',false);
        $.ajax(
        {
            url:'/time/elapsed/'+id,
            dataType:'json',
            data:form_data,
            contentType:false,
            cache:false,
            processData:false,
            success:function(callback)
            {
              if(callback.valid)
              {
                $('.small-model').modal('show');
                $('.small-model').find('.modal-title').text('Success');
                $('.small-model').find('.modal-body').html('<div class="text-success text-center"><i class="fa fa-check-circle"></i> '+callback.message+'.</div>');
              }
              else
              {
                $('.small-model').modal('show');
                $('.small-model').find('.modal-title').text('Warning');
                $('.small-model').find('.modal-body').html('<div class="text-warning text-center"><i class="fa fa-exclmation-circle"></i> '+callback.message+'</div>');
                $(document).find('.exam input').attr('disabled',true);
                $(document).find('.exam button:last').attr('disabled',true);
              }
            },
            error(err)
            {
              console.log(err.status+':'+err.statusText);
            }
        });
    } 
    else 
    {
        time = new Date(msLeft);
        hours = time.getUTCHours();
        mins = time.getUTCMinutes();
        seconds=time.getUTCSeconds();
        element.innerHTML = (hours ? hours + ':' + twoDigits(mins) : mins) + ':' + twoDigits(seconds);

        /* Save current time locally*/
        localStorage.setItem('lastHValue', hours);
        localStorage.setItem('lastMValue', mins);
        localStorage.setItem('lastSValue', time.getUTCSeconds());

        myTimeout=setTimeout(updateTimer, time.getUTCMilliseconds() + 500);
    }
}

if (localStorage.getItem('lastHValue')) 
{
    let lastHValue = parseInt(localStorage.getItem('lastHValue')),
        lastMValue = parseInt(localStorage.getItem('lastMValue')),
        lastSValue = parseInt(localStorage.getItem('lastSValue'));

    let totalMValue = parseInt((lastHValue * 60) + lastMValue);
    countdown('countdown', totalMValue, lastSValue);
}

$(document).on('click','#start-exam',function()
{
    var dbtime=$(document).find('#quiz_time').val();
    $(this).parent().parent().parent().hide().next().show();
    sessionStorage.intro=true;
    localStorage.setItem('lastHValue', 0);
    localStorage.setItem('lastMValue', 40);
    //localStorage.setItem('lastMValue', parseInt(dbtime));
    localStorage.setItem('lastSValue', 60);
    //countdown('countdown',parseInt(dbtime), 59);
    countdown('countdown',40, 59);
});


$(document).on('change','input[type=file]',function()
{
  $(this).removeClass('is-invalid').addClass('is-valid').parent().find('label').removeClass('invalid-feedback').addClass('valid-feedback').html('Filename: '+this.files[0].name);
}); 

$(document).on('click','.nextBtn',function()
{
    var parent=$('#answers'),
    list=parent.children();
    while(list.length)
    {
      parent.append(list.splice(Math.floor(Math.random() * list.length), 1)[0]);
    }
    $(this).parents('form').hide();
    $(this).parents('form').next().show();
});


$(document).on('click','.prevBtn',function()
{
    $(this).parents('form').hide();
    $(this).parents('form').prev().show();
});

$(document).ready(function()
{
    var parent=$('#answers'),
    list=parent.children();
    while(list.length)
    {
      parent.append(list.splice(Math.floor(Math.random() * list.length), 1)[0]);
    }
});

/*ActiveForm*/
$(document).on('submit','.ActiveForm',function()
{
    var el=$(this),
    urlparams=new URLSearchParams(window.location.search),
    next=urlparams.get('next'),
    btn_txt=el.find('button:last').html(),
    form_data=new FormData(this);
    $('.feedback').html('');
    el.children().find('.is-invalid').removeClass('is-invalid');
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
        el.find('button:last').html('<i class="spinner-border spinner-border-sm" role="status"></i> Please wait...').attr('disabled',true);
      },
      xhr:function()
      {
        const xhr=new window.XMLHttpRequest();
        xhr.upload.addEventListener('progress',function(e)
        {
          if(e.lengthComputable)
          {
            const percent=Math.round((e.loaded/e.total)*100);
            el.find('button:last').html('<i class="spinner-border spinner-border-sm" role="status"></i> Please wait '+percent+'% ...').attr('disabled',true);
          }
        });
        return xhr
      },
      success:function(callback)
      {
        el.find('button:last').html(btn_txt).attr('disabled',false);
        if(callback.topup)
        {
          $('.small-model').modal({show:true});
          $('.small-model').find('.modal-title').text('Info');
          $('.small-model').find('.modal-body').html('<div class="text-success text-center"><i class="fa fa-check-circle"></i> '+callback.message+'.</div>');
          $('.small-model').find('.row').html(`<div class="col-12 text-center"><a href="/account/topup?amount=${callback.money}" class="btn btn-round btn-primary btn-block"><i class="ti-money"></i> Topup ${callback.money}</a></div>`)
        }
        if(callback.valid)
        {            
            el[0].reset();
            if(callback.whatsapp)
            {
              var phone=document.getElementById('phone').value,
              text=encodeURI("Hello Peter, my name is Kevin I have submitted exam/quiz order with the following details:\nOrder id:#"+callback.id+"\nTopic:"+callback.topic+"\nNumber of MCQ Questions:"+callback.mcq+"\nNumber of Essay questions:"+callback.no_essay+"\nCountry:"+callback.country);
              $('.small-model').modal({show:true});
              $('.small-model').find('.modal-title').text('Success');
              $('.small-model').find('.modal-body').html('<div class="text-success text-center"><i class="fa fa-check-circle"></i> '+callback.message+'.WhatsApp exam department admin</div>');
              $('.small-model').find('.row').html(`<div class="col-12 text-center"><a href="https://api.whatsapp.com/send?phone=${phone}&text=${text}" class="btn btn-round btn-primary btn-block" target="_blank"><i class="fa fa-whatsapp"></i> Whatsapp exam dept</a></div>`)
            }
            else if(callback.new_message)
            {
              el.find("input[aria-label='message']").parents('.wrapper').find('.feedback').css('color','#5cb85c !important').html('<i class="fa fa-check-circle"></i> '+callback.new_message);
              if($('.chat_windows ul').children('li').length > 0)
              {
                $('.chat_windows ul').append(`<li class="my-message">
                                            <img class="avatar mr-3" src="${callback.profiler}"    alt="${callback.name}">
                                            <div class="message">
                                                <p class="bg-light-blue">${callback.submitted_message}</p>
                                                <span class="time" >${callback.time}</span>
                                            </div>
                                        </li>`);
              }
              else
              {
                 $('.chat_windows ul').html(`<li class="my-message">
                                            <img class="avatar mr-3" src="${callback.profiler}"    alt="${callback.name}">
                                            <div class="message">
                                                <p class="bg-light-blue">${callback.submitted_message}</p>
                                                <span class="time" >${callback.time}</span>
                                            </div>
                                        </li>`);
              }
            }
            else
            {
              $('.small-model').modal({show:true});
              $('.small-model').find('.modal-title').text('Success');
              $('.small-model').find('.modal-body').html('<div class="text-success text-center"><i class="fa fa-check-circle"></i> '+callback.message+'.</div>');
            }
            if(callback.verdict)
            {
              $(document).find('select[name="verdict"]').parents('table').find('tr').not('tr:first,tr:last').show(); 
            } 
            if(callback.completed)
            {
              el.find('button:first').attr('disabled',true).html(`<i class="ti-check"></i> Order Completed`);
            }
            if(callback.order_update)
            {
              $(document).find('.all-bids a:last').replaceWith(`<button class="btn btn-round btn-success btn-sm" disabled><i class="ti-check"></i> select</button>`);
            }  
            if(callback.accept_bid)
            {
              el.find('button:first').attr('disabled',true).html(`<i class="ti-hand-open"></i> Bid Accepted`);
            }
            if(callback.bid)
            {
              el.find('button:last').attr('disabled',true);
            } 
            if(callback.essay)
            {
              window.location='/go/to/dashboard/'+callback.id;
            }
            if(callback.answered)
            {
              if(!el.next().html())
              {
                clearTimeout(myTimeout)
                localStorage.removeItem('lastHValue');
                localStorage.removeItem('lastMValue');
                localStorage.removeItem('lastSValue');
                sessionStorage.removeItem('intro');
                el.find('button:last').hide();
                el.find('.float-right').append('<a class="btn btn-primary btn-round" href="/write/essay/'+callback.id+'">Finish <i class="ti-arrow-right"></i></a>')
              }
              else
              {
                el.find('button:last').removeClass('submitBtn').addClass('nextBtn').attr('type','button').html('next <i class="ti-arrow-right"></i>')
              }
            }
            if(callback.profile)
            {
              if(callback.category =='customer')
              {
                window.location='/profile/setup/complete';
              }
              else
              {
                window.location='/grammer/test/'+callback.id;
              }
            }
            if(callback.register)
            {
              if(callback.category)
              {
                window.location='/accounts/activate/'+callback.category;
              }
            } 
            if(callback.login)
            {
                if(next)
                {
                    window.location=next;
                }
                else
                {
                    window.location='/dashboard';
                }
            }
        }
        else
        {
            $.each(callback.uform_errors,function(key,value)
            {
              el.find("input[aria-label='"+key+"'],select[aria-label='"+key+"'],textarea[aria-label='"+key+"']").addClass('is-invalid').parents('.form-group,.wrapper').find('.feedback').addClass('text-danger').html('<i class="fa fa-exclamation-circle"></i> '+value);
            });
            $.each(callback.eform_errors,function(key,value)
            {
              el.find("input[aria-label='"+key+"'],textarea[aria-label='"+key+"'],select[aria-label='"+key+"']").addClass('is-invalid').parents('.form-group,.wrapper').find('.feedback').addClass('text-danger').html('<i class="fa fa-exclamation-circle"></i> '+value);
            });

            if(callback.permission)
            {
                $('.delete-model').modal({show:true});
                $('.delete-model').find('.modal-title').html('<div class="text-warning">Warning</div>');
                $('.delete-model').find('.modal-body').html('<div class="text-info text-center"><i class="fas fa-exclamation-triangle"></i>'+callback.message+'</div>');
            }
        }
        if(callback.error)
        {
            $('.small-model').modal({show:true});
            $('.small-model').find('.modal-title').text('Info');
            $('.small-model').find('.modal-body').html('<div class="text-info text-center"><i class="fas fa-exclamation-triangle"></i> No changes made.</div>');
        }
        if(callback.status)
        {
            window.location='/suspended/account';
        }
      },
      error:function(err)
      {
        el.find('button:last').html(btn_txt).attr('disabled',false);
      }
    });
  return false;
});




/*ProfileForm*/
$(document).on('submit','.ProfileImageForm',function()
{
  var el=$(this),
  form_data=new FormData(this);
  $('.feedback').html('');
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
        $('.uploadBtn').html('<i class="spinner-border spinner-border-sm"></i> Please wait...');
      },
      xhr:function()
      {
        const xhr=new window.XMLHttpRequest();
        xhr.upload.addEventListener('progress',function(e)
        {
          if(e.lengthComputable)
          {
            const percent=Math.round((e.loaded/e.total)*100);
            $('.uploadBtn').html('<i class="spinner-border spinner-border-sm"></i> Uploading '+percent+'% ...').attr('disabled',true);
          }
        });
        return xhr
      },
      success:function(callback)
      {
        $('.uploadBtn').removeClass('uploadBtn').addClass('getprofilepic').html('<i class="ti-camera"></i> Change picture').attr({'type':'button','disabled':false});
        if(callback.valid)
        {
            $('.small-model').modal({show:true});
            $('.small-model').find('.modal-title').text('Success');
            $('.small-model').find('.modal-body').html('<div class="text-success text-center"><i class="fa fa-check-circle"></i> '+callback.message+'.</div>');
            el[0].reset();
          }
        else
        {
            $.each(callback.uform_errors,function(key,value)
            {
              el.find("input[aria-label='"+key+"']").addClass('is-invalid').parents('.form-group').find('.feedback').addClass('invalid-feedback').html('<i class="fa fa-exclamation-circle"></i> '+value);
            });
        }
        if(callback.error)
        {
            $('.small-model').modal({show:true});
            $('.small-model').find('.modal-title').text('Info');
            $('.small-model').find('.modal-body').html('<div class="text-info text-center"><i class="fas fa-exclamation-triangle"></i> No changes made.</div>');
        }
      },
      error:function(err)
      {
        $('.uploadBtn').removeClass('uploadBtn').addClass('getprofilepic').html('<i class="ti-camera"></i> Change picture').attr({'type':'button','disabled':false});
        console.log(err.status+':'+err.statusText);
      }
    });
  return false;
});

$(document).on('click','.getprofilepic',function()
{
    var el=$(this);
    el.removeClass('getprofilepic').addClass('uploadBtn').html('<i class="spinner-border spinner-border-sm"></i> Please wait...');
    $('#id_profile_pic').click();
});

$(document).on('click','.formuploadBtn',function()
{
    var el=$(this);
    el.attr('disabled',true).html('<i class="spinner-border spinner-border-sm"></i> Please wait...');
    $('#id_profile_pic').click();
});

$(document).on('change','.profile',function()
{
    var el=$(this),
    file=el.get(0).files[0],
    ext=el.val().substring(el.val().lastIndexOf('.')+1).toLowerCase();
    $('.uploadbtn').removeClass('spinner-border spinner-border-sm').addClass('ti-upload');
    if(file && (ext=='jpg' || ext=='png' || ext=='jpeg' || ext=='gif'))
    {
        var reader=new FileReader();
        reader.onload=function(e)
        {
            $('.imagecard').find('img:last').attr('src',reader.result);
            $('.uploadBtn').html('<i class="ti-upload"></i> Upload').attr('type','submit');
            $('.formuploadBtn').html('<i class="ti-camera "></i> Upload picture').attr('disabled',false);
        }
        reader.readAsDataURL(file);
    }
    else
    {
      $('.small-model').modal({show:true});
      $('.small-model').find('.modal-title').text('Warning');
      $('.small-model').find('.modal-body').html('<div class="text-warning text-center"><i class="zmdi zmdi-alert-triangle"></i> Invalid image format</div>');
    }
});

/*ActiveForm*/
$(document).on('submit','.UploadForm',function()
{
  var el=$(this),
  form_data=new FormData(this);
  $('.feedback').html('');
  el.children().find('.is-invalid').removeClass('is-invalid');
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
        el.find('button:last').attr('disabled',true).html('<i class="spinner-border spinner-border-sm" role="status"></i> Please wait...');
      },
      xhr:function()
      {
        const xhr=new window.XMLHttpRequest();
        xhr.upload.addEventListener('progress',function(e)
        {
          if(e.lengthComputable)
          {
            const percent=Math.round((e.loaded/e.total)*100);
            el.find('button:last').html('<i class="spinner-border spinner-border-sm" role="status"></i> Uploading '+percent+'% ...');
          }
        });
        return xhr
      },
      success:function(callback)
      {
        el.find('button:last').attr('disabled',false).html('submit');
        if(callback.valid)
        {
            $('.small-model').modal({show:true});
            $('.small-model').find('.modal-title').text('Success');
            $('.small-model').find('.modal-body').html('<div class="text-success text-center"><i class="fa fa-check-circle"></i> '+callback.message+'.</div>');
            el.find('small').html('');
            $('.dropify-clear').click();
            el[0].reset();
            if(callback.project_id)
            {
              window.location='/add/pictures/'+callback.project_id+'/';
            }
          }
        else
        {
            $.each(callback.uform_errors,function(key,value)
            {
              el.find("input[aria-label='"+key+"'],textarea[aria-label='"+key+"']").addClass('is-invalid').parents('.form-group').find('.feedback').addClass('invalid-feedback').html('<i class="fa fa-exclamation-circle"></i> '+value);
            });
        }
        if(callback.error)
        {
            $('.small-model').modal({show:true});
            $('.small-model').find('.modal-title').text('Info');
            $('.small-model').find('.modal-body').html('<div class="text-info text-center"><i class="fas fa-exclamation-triangle"></i> No changes made.</div>');
        }
      },
      error:function(err)
      {
        el.find('button:last').attr('disabled',false).html('submit');
      }
    });
  return false;
});

$(document).on('change','.fileinput',function()
{
    var el=$(this),
    file=el.get(0).files[0],
    ext=el.val().substring(el.val().lastIndexOf('.')+1).toLowerCase();
    if(file && (ext=='zip' || ext=='rar'))
    {
        return true;
    }
    else
    {
      $('.small-model').modal({show:true});
      $('.small-model').find('.modal-title').text('Warning');
      $('.small-model').find('.modal-body').html('<div class="text-warning text-center"><i class="zmdi zmdi-alert-triangle"></i> Invalid image format</div>');
      $('.dropify-clear').click();
    }
});

$(document).on('change','input[type=file]',function()
{
  $(this).removeClass('is-invalid').addClass('is-valid').parent().find('.feedback').removeClass('invalid-feedback').addClass('valid-feedback').html('Filename: '+this.files[0].name);
});


$(document).on('click','.del-data',function(e)
{
  e.preventDefault();
  var el=$(this);
  $('.delete-model').modal({show:true});
  $('.delete-model').find('.modal-title').text('Confirm');
  if(el.data('text')!=undefined)
  {
    $('.delete-model').find('.modal-body').html('<div class="text-warning text-info text-center"><i class="fa fa-alert-triangle"></i> '+el.data('text')+' .</div> <div class="text-center"><button class="btn btn-secondary btn-round cancelBtn" data-dismiss="modal">cancel</button><button data-host="'+el.data('host')+'" data-url="'+el.attr('href')+'"  class="btn btn-danger btn-round confirmBtn">confirm</button></div>');
  }
  else
  {
      $('.delete-model').find('.modal-body').html(`<div class="text-warning text-info text-center"><i class="fa fa-alert-triangle"></i> Confirm deleting item .</div><div class="row"><div class="col-12 text-center"><button class="btn btn-secondary btn-round" data-dismiss="modal">cancel</button><button style="background:#d64242 !important" data-host="${el.data('host')}" data-url="${el.attr('href')}" class="btn btn-danger btn-round confirmBtn">confirm</button></div></div>`);
  }
});

$(document).on('click','.cancelBtn',function()
{
  $(this).parents('.modal').find('.close').click();
});

$(document).on('click','.confirmBtn',function()
{
  var el=$(this),
  btn_text=el.html();
  url=el.data('url');
  $.ajax(
      {
        url:url,
        dataType:'json',
        beforeSend:function()
        {
          el.html('<i class="spinner-border spinner-border-sm" role="status"></i> Please wait...');
        },
        success:function(callback)
        {
          el.html(btn_text);
          $('.delete-model').modal('hide');
          refreshPage(el,el.data('host'),'table-results');
          var counter=$('#id_'+callback.id).parents('.card').find('.spanner').html();
          if(parseInt(counter) > 0)
          {
            $('#id_'+callback.id).parents('.card').find('.spanner').html(parseInt(counter) - 1);
          }
          else
          {
            $('#id_'+callback.id).parents('.card').find('.spanner').html("0");
          }
          if($('#id_'+callback.id).children('.row').length > 0)
          {
            $('#id_'+callback.id).remove();
          }
          else
          {
            $('#id_'+callback.id).html(`<div class="col-12 text-center my-auto"><h4><i class="ti-info-alt"></i> No data found</h4></div>`);
          }
          if(callback.valid)
          {
            $('.small-model').modal('show');
            $('.small-model').find('.modal-title').text('Success');
            $('.small-model').find('.modal-body').html('<div class="text-success text-center"><i class="fa fa-check-circle"></i> '+callback.message+'.</div>');
          }
          else
          {
            $('.small-model').modal('show');
            $('.small-model').find('.modal-title').text('Warning');
            $('.small-model').find('.modal-body').html('<div class="text-warning text-center"><i class="fa fa-exclmation-circle"></i> '+callback.message+'</div>');
            if(callback.topup)
            {
              $('.small-model').find('.modal-body').append(`<div class="text-center mt-2"><a href="/account/topup" class="btn btn-info btn-round"><i class="ti-money"></i> Topup</a></div>`);
            }
          }
        },
        error(err)
        {
          el.html(btn_text);
          console.log(err.status+':'+err.statusText);
        }
      });
});

/*refreshPage*/
function refreshPage(wrapper,url, target)
{
    $.ajax(
    {
      url:url,
      context:this,
      dataType:'html',
      success:function(callback)
      {
        $(document).find('.'+target).html($(callback).find('.'+target).html());
        observerImages();
      },
      error:function(err)
      {
        console.log(err.status+':'+err.statusText);
      }
    });
}


$(document).on('click','.btn-darkmode',function()
{
  localStorage.darkmode=$(this).is(":checked");
});
$(document).on('click','.btn-sidebar',function()
{
  localStorage.sidebar=$(this).is(":checked");
});
$(document).on('click','.btn-min_sidebar',function()
{
  localStorage.min_sidebar=$(this).is(":checked");
});
$(document).on('click','.btn-iconcolor',function()
{
  localStorage.iconcolor=$(this).is(":checked");
});
$(document).on('click','.btn-gradient',function()
{
  localStorage.gradient=$(this).is(":checked");
});
$(document).on('click','.btn-boxlayout',function()
{
  localStorage.boxlayout=$(this).is(":checked");
});
$(document).on('click','.btn-boxshadow',function()
{
  localStorage.boxshadow=$(this).is(":checked");
});
$(document).on('click','.btn-fixnavbar',function()
{
  localStorage.fixnavbar=$(this).is(":checked");
});
$(document).on('click','.btn-pageheader',function()
{
  localStorage.pageheader=$(this).is(":checked");
});

$(document).on('click','input[name=font]',function()
{
  localStorage.fontname=$(this).val();
});

$(document).ready(function ()
{  
    observerImages();
    /*fontname*/
    if(localStorage.getItem("fontname") == 'true')
    {
      $('body').addClass(localStorage.getItem("fontname"));
      $(document).find('input[value="'+localStorage.getItem("fontname")+'"]').prop('checked',true);
    }
    else
    {
      $('body').addClass(localStorage.getItem("fontname"));
      $(document).find('input[value="'+localStorage.getItem("fontname")+'"]').prop('checked',false);
    }
    /*dark-mode*/
    if(localStorage.getItem("darkmode") == 'true')
    {
      $('body').addClass("dark-mode");
      $(document).find('.btn-darkmode').prop('checked',true);
    }
    else
    {
      $('body').removeClass("dark-mode");
      $(document).find('.btn-darkmode').prop('checked',false);
    }

    /*sidebar_dark*/
    if(localStorage.getItem("sidebar")  == 'true')
    {
      $('body').addClass("sidebar_dark");
      $(document).find('.btn-sidebar').prop('checked',true);
    }
    else
    {
      $('body').removeClass("sidebar_dark");
      $(document).find('.btn-sidebar').prop('checked',false);
    }

    /*minsidebar*/
    if(localStorage.getItem("min_sidebar")  == 'true')
    {
      $('#header_top').addClass("dark");
      $(document).find('.btn-min_sidebar').prop('checked',true);
    }
    else
    {
      $('#header_top').removeClass("dark");
      $(document).find('.btn-min_sidebar').prop('checked',false);
    }

    /*iconcolor*/
    if(localStorage.getItem("iconcolor")  == 'true')
    {
      $('body').addClass("iconcolor");
      $(document).find('.btn-iconcolor').prop('checked',true);
    }
    else
    {
      $('body').removeClass("iconcolor");
      $(document).find('.btn-iconcolor').prop('checked',false);
    }

     /*gradient*/
    if(localStorage.getItem("gradient")  == 'true')
    {
      $('body').addClass("gradient");
      $(document).find('.btn-gradient').prop('checked',true);
    }
    else
    {
      $('body').removeClass("gradient");
      $(document).find('.btn-gradient').prop('checked',false);
    }

    /*boxlayout*/
    if(localStorage.getItem("boxlayout")  == 'true')
    {
      $('body').addClass("boxlayout");
      $(document).find('.btn-boxlayout').prop('checked',true);
    }
    else
    {
      $('body').removeClass("boxlayout");
      $(document).find('.btn-boxlayout').prop('checked',false);
    }

    /*boxshadow*/
    if(localStorage.getItem("boxshadow")  == 'true')
    {
      $(document).find('.notification a').addClass("box_shadow");
      $(document).find('.btn-boxshadow').prop('checked',true);
    }
    else
    {
      $(document).find('.notification a').removeClass("box_shadow");
      $(document).find('.btn-boxshadow').prop('checked',false);
    }

    /*fixnavbar*/
    if(localStorage.getItem("fixnavbar")  == 'true')
    {
      $('#page_top').addClass("sticky-top");
      $(document).find('.btn-fixnavbar').prop('checked',true);
    }
    else
    {
      $('#page_top').removeClass("sticky-top");
      $(document).find('.btn-fixnavbar').prop('checked',false);
    }

    /*pageheader*/
    if(localStorage.getItem("pageheader")  == 'true')
    {
      $('#page_top').addClass("top_dark");
      $(document).find('.btn-pageheader').prop('checked',true);
    }
    else
    {
      $('#page_top').removeClass("top_dark");
      $(document).find('.btn-pageheader').prop('checked',false);
    }

    if(sessionStorage.getItem('intro') == 'true')
    {
        $(document).find('.intro').hide().next().show();
    }

    $('.exam').find('form').not('form:first').hide();
    $('.exam').find('form:first').append('<div class="float-right"><button class="btn btn-primary btn-round submitBtn" disabled>save answer <i class="ti-arrow-up"></i></button></div>');

    $('.exam').find('form').not('form:first').not('form:last').append('<div class="float-right"><button type="button" class="btn btn-primary btn-round prevBtn"><i class="ti-arrow-left"></i> prev</button> <button class="btn btn-primary btn-round submitBtn" disabled>save answer <i class="ti-arrow-up"></i></button></div>');
    $('.exam').find('form:last').append('<input type="text"name="lastpage" value="1" hidden><div class="float-right"><button type="button" class="btn btn-primary btn-round prevBtn"><i class="ti-arrow-left"></i> prev</button> <button class="btn btn-primary btn-round submitBtn" disabled>save answer <i class="ti-arrow-up"></i></button></div>');
    
    $(document).on('change','.exam input[type=radio]',function()
    {
      $(this).parents('form').find('button:last').attr('disabled',false);
      $(this).parents('form').find('input[type=radio]').not(':checked').attr('disabled',true);
    });
});


/*approveBtn*/
$(document).on('click','.approveBtn',function()
{
  var el=$(this)
  if(sessionStorage.getItem('mychoice') =='true')
  {

    el.removeClass('approveBtn').addClass('confirmBtn').click();
  }
  else
  {
    $('.delete-model').modal({show:true});
    $('.delete-model').find('.modal-title').text('Confirm Approving Order');
    $('.delete-model').find('.modal-body').html('<div class="text-warning text-info text-center"><i class="fa fa-alert-triangle"></i> Confirm approving order '+el.data('order')+' .</div> <div class="text-center"><button class="btn btn-secondary cancelBtn" >cancel</button><button data-host="'+el.data('host')+'" data-url="'+el.data('url')+'" class="btn btn-danger confirmBtn">confirm</button></div><br><div class="form-check"><input class="form-check-input" id="mychoice" type="checkbox"><label class="form-check-label"  for="mychoice">Remember My choice</label></div>');
  }

});

$(document).on('change','#mychoice',function()
{
  sessionStorage.mychoice=true;
});
