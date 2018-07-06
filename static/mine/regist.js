var isSubmitable = false;

function showError(msg, isUseLabel) {
    var errorP = this.parentElement.nextElementSibling
    errorP.innerText = isUseLabel ? this.title : msg;

    $(errorP).fadeIn();
    $(this.parentElement).addClass('has-error');

    $(this).focus(function () {
        $(errorP).fadeOut();
        $(this.parentElement).removeClass('has-error');
    });
}

$(function () {
    $('input').blur(function () {
        if (this.value.trim().length == 0) {
            showError.call(this, '不能为空', true);
            console.log('不能为空')
            return
        } else {
            $(this).parent().removeClass('has-error');
            $(this).parent().next().fadeOut();
        }

        if (this.name == 'username' &&
            this.value.trim().length < 6) {
            showError.call(this, this.placeholder, true);
            return
        }

        if (this.name == 'passwd' &&
            this.value.trim().length < 6) {
            showError.call(this, this.placeholder, true);
            return
        }

        if (this.name == 'passwd2') {
            var passwd1 = $('input[name=passwd]').val()
            console.log('口令1： ', passwd1);
            if (this.value.trim() != passwd1.trim())

                showError.call(this, '两次口令不相同！', false);
            return
        }
        isSubmitable = true;
    })
})

function submitForm() {
    var inputs = $('input')
    // 验证是否为空的
    for (var i = 0; i < inputs.length; i++) {
        var input = inputs.get(i)
        if ($(input).val().trim() == '') {
            $(input).parent().addClass('has-error');
            $(input).parent().next().fadeIn()
            return
        } else {
            $(input).parent().removeClass('has-error');
            $(input).parent().next().fadeOut()
        }
    }

    if (isSubmitable)
        $('form').submit();  // 提交注册
    console.log('--check regist----');
}