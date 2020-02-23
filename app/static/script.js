var protocol, mailbox;

$('body').ready(function(){
  protocol = $('#content').attr('protocol');
  mailbox = $('#content').attr('mailbox');
})

// change state all of checkboxes
$('#m').change(function(){
  if ($(this).prop('checked')){
    $("input[type=checkbox]").prop('checked', true);
  }
  else {
    $("input[type=checkbox]").prop('checked', false);
  }
})

// change state of control buttons
$('.mail-check').change(function(){
  count = $('.reg_mail:checked').length;
  if (count == 0){
    $('.control-button').addClass('disabled');
  }else {
    $('.control-button').removeClass('disabled');
  }
})

// submit form
$('.control-button').click(function(){
  let form = $('form');
  let sender = $(this);
  if (!sender.hasClass('disabled')){
      form.attr('action', '/' + protocol + '/' + mailbox + '/mark/' + sender.attr('id') + '/');
      form.submit();
  }
})
