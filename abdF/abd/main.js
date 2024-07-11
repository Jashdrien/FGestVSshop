$('.modal').on('show.bs.modal', function(e) {
    $('.modal').not(this).modal('hide');
});