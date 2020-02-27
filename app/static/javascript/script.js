var inputs = document.querySelectorAll('.file');
Array.prototype.forEach.call(inputs, function(input){
  var label	 = input.nextElementSibling,
      labelVal = label.innerHTML;
  input.addEventListener('change', function(e){
    var fileName = '';
    if( this.files && this.files.length > 1 )
      fileName = ( this.getAttribute( 'data-multiple-caption' ) || '' ).replace( '{count}', this.files.length );
    else
      fileName = e.target.value.split( '\\' ).pop();
		if( fileName )
      label.querySelector( 'span' ).innerHTML = fileName;
    else
      label.innerHTML = labelVal;
	});
});

var protocol, mailbox;

$('.errors, .notifications').click(function(){
  $(this).hide('slow');
})

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
      if (protocol == 'imap'){
          form.attr('action', '/' + protocol + '/' + mailbox + '/mark/' + sender.attr('id') + '/');
      }
      else{
        form.attr('action', '/' + protocol + '/mark/' + sender.attr('id') + '/');
      }
      form.submit();
  }
})
