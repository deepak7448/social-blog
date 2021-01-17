$(document).ready(function(){
$('.dropdown ')
.dropdown({
    transition: 'scale ',
    action: 'hide '
    });
$('.ui.accordion ')
.accordion
    .accordion({
    selector: {
    trigger: '.title .icon '
    }
});
  tinymce.init({
  selector: '#content',
  mode: "textareas",
  plugins: "emoticons",
  toolbar: 'emoticons',
});
});
