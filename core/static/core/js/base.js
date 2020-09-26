$(document).ready(function(){
    let profileWrapper = $('#user-profile-wrapper-id');
    let profileArrowId = $('#arrow-id');
    let loginForm = $('#login-form-id');
    let signUpForm = $('#register-form');
    let loginEmailForm = $('#email');
    let emailForm = $('#user-email');
    let passwordForm1 = $('#user-password1');
    let passwordForm2 = $('#user-password2');


    let successModal = $('#user-registered-success-modal-id')

    //hamburger button

    $("#hamburger-id").click(function (e) {
        $("#side-bar-id").fadeIn(100)
        $("#close-side-bar-id").fadeIn(100)
        $('body').css('overflow', 'hidden');





    })

    $("#close-side-bar-id").click(function (e) {
        $("#side-bar-id").fadeOut()
        $("#close-side-bar-id").fadeOut()
        $('body').css('overflow', 'auto');


    })

    // Book Category

    $(".side-bar-category-wrapper-main").each(function () {
        $(this).mouseenter(function (e) {
                $(this).children('.side-bar-category-details-wrapper').show()
                $(this).children('.side-bar-category').children('.arrow-svg').show()

        })

        $(this).mouseleave(function (e) {

            $(this).children('.side-bar-category-details-wrapper').hide()
            $(this).children('.side-bar-category').children('.arrow-svg').hide()

        })
    })


    //Rating

    $('.fa').each(function(){
        $(this).mouseenter(function (e) {
            $(this).addClass('checked')
            $(this).prevAll('.fa').addClass('checked')


        })

        $(this).mouseleave(function (e) {
            $(this).removeClass('checked')
            $(this).prevAll('.fa').removeClass('checked')


        })

        $(this).click(function (e) {
            e.preventDefault();
            $(this).addClass('clicked-checked')
            $(this).prevAll('.fa').addClass('clicked-checked')
            $(this).nextAll('.fa').removeClass('clicked-checked')
            let ratingCount = (($(this).prevAll('.fa')).length)+1;
            let endPoint= '/home/rating/'+$("#book-slug").text()+'/'
             console.log(ratingCount)


            $.ajax({
                headers: { "X-CSRFToken": $.cookie("csrftoken") },
                url: endPoint,
                method: 'post',
                success: function (data) {
                    console.log(data.slug_name)

                },
                data: {
                    'rating_count': ratingCount,
                }




                }

            )

        })

    })





    $("input").keypress(function(e){
        $("input").nextAll('p').empty()
    });

    $("#close-message-pop-id").click(function(e){
        $("#message-wrapper-id").hide();
        $("#user-profile-wrapper-id").removeClass('no-view');
        $("#arrow-id").removeClass('no-view');
    })

    $("#close-user-registered-message-pop-id").click(function(e){
        $("#user-registered-success-modal-id").hide();



    })


      $(".rent-link").each(function(){
          $(this).click(function(e){
              e.preventDefault();

              let endPoint = $(this).attr('href')
              console.log(endPoint)

               $.ajax({
                   url: endPoint,

                   success: function(data){
                       console.log(data.book)
                       if(data.book){
                           $("#the-book-modal-id").fadeIn();

                           $("#book-title-id").text(data.book.title)
                           $("#book-author-id").text(data.book.author)
                           $("#book-img-id").attr('src', data.book.image)
                           $("#book-summary").text(data.book.summary)
                           $("#book-condition-span-id").text(data.book.book_condition)
                           $("#book-quality-rating-span-id").text(data.book.quality_rating)
                           $("#book-slug").text(data.book.slug)
                           $("#published-date-id").text(data.book.published_date)
                           $("#page-count-id").text(data.book.page_count)
                           $('#book-genre-span-id').text(data.book.book_genre)
                           $('#book-rating-id').text(data.book.book_rating)
                           let count = 1
                           $(".fa").each(function (e) {

                               if(count <= data.book.my_rating){
                                   $(this).addClass('clicked-checked')
                                   count++;

                               }


                           })


                           $('body').css('overflow', 'hidden');

                           




                       }


                   }

               }






               )

          });
    });

    $("#close-book-modal-id").click(function(e){

        $('#the-book-modal-id').hide();
        $('#book-img-id').attr('src','')
        $('.fa').each(function (){
            $(this).prevAll('.fa').removeClass('clicked-checked')
            $(this).removeClass('clicked-checked')
            $(this).nextAll('.fa').removeClass('clicked-checked')
        })
        $('body').css('overflow', 'auto');



    })



    signUpForm.submit(function(event) {
        event.preventDefault();
        let endPoint = signUpForm.attr('action')
        let httpMethod = signUpForm.attr('method')
        let formData = signUpForm.serialize();
        $('#user-profile-submit-button-id-signup').hide();
        $('#submit-button-load-id').removeClass('no-view')




        $.ajax({
            headers: { "X-CSRFToken": $.cookie("csrftoken") },
            url: endPoint,
            method: httpMethod,
            data: formData,
            mode: 'same-origin',
            success: function(data) {
                console.log(data)
                $("input").nextAll('p').empty()
                if (data.form_error_message) {

                    if (data.form_error_message.email) {
                        emailForm.after('<p style="color: red; font-size: 14px;">' + data.form_error_message.email + '</p>')
                    }
                    if (data.form_error_message.password1) {
                        passwordForm1.after('<p style="color: red; font-size: 14px;">' + data.form_error_message.password1 + '</p>')
                    }
                    if (data.form_error_message.password2) {
                        passwordForm1.after('<p style="color: red; font-size: 14px;">' + data.form_error_message.password2 + '</p>')
                    }

                    $('#user-profile-submit-button-id-signup').show();
                    $('#submit-button-load-id').addClass('no-view')
                }

                if (data.registered === true){
                    signUpForm.trigger("reset");
                    $('#user-profile-submit-button-id-signup').show();
                    $('#submit-button-load-id').addClass('no-view')

                    profileWrapper.addClass('no-view');
                    profileArrowId.addClass('no-view');

                    successModal.removeClass('no-view');
                    $('#success-message-display-id').text(data.messages)
                    // successModal.html('<p class="success-message-display">'+data.messages+'</p>');
                }
            },
            error: function(errorData){
                console.log("errorloss")
                console.log(errorData.form_error_message)
            }
        })
    })


    loginForm.submit(function(event){
        event.preventDefault();
        let endPoint = loginForm.attr('action')
        let httpMethod = loginForm.attr('method')
        let formData = loginForm.serialize();

        $.ajax({
            headers: { "X-CSRFToken": $.cookie("csrftoken") },
            url: endPoint,
            method: httpMethod,
            data: formData,
            mode: 'same-origin',
            success: function(successData){
                 if(successData.logged_in === 'true'){
                    window.location.href = 'http://kitabalaya.com:8000/home/'

                }
                 else{
                     $("input").nextAll('p').empty();
                     if(successData.messages) {
                         loginEmailForm.after('<p style="color: red; font-size: 14px;">' + successData.messages + '</p>')
                     }
                 }
            },
            error: function(errorData){
                console.log("error")
                console.log(errorData)
            }
        })
    })
})





































let search_button = document.getElementById('search-img')
let search_end = document.getElementById('search-end')
let search_box = document.getElementById('searchbox')
let secondary_nav_book_list_category = document.getElementById('book-list-category-id')
let banner_wrapper = document.getElementById('banner-img-id')

let hamburger = document.getElementById('hamburger-id');
let side_bar = document.getElementById('side-bar-id');




const user_profile = document.getElementById('user-profile-wrapper-id');

const user_sign_in = document.getElementById('user-sign-in-wrapper-id');
const user_sign_up = document.getElementById('user-sign-up-wrapper-id');



const user_profile_button = document.getElementById('accounts-id');
const user_profile_arrow_id = document.getElementById('arrow-id');

const user_cart = document.getElementById('user-cart-wrapper-id');
const user_cart_button = document.getElementById('cart-id');
const user_cart_id = document.getElementById('arrow-cart-id');


const register_btn = document.getElementById('user-register')
const  user_register = document.getElementById('user-profile-register-wrapper-id')
const  login_btn = document.getElementById('user-login')

if(user_profile_button){
user_profile_button.addEventListener('click', ()=>{
    user_profile.classList.toggle('no-view');
    user_profile_arrow_id.classList.toggle('no-view');


    if(user_cart.classList.contains('no-view')){
       
    }
    else{
        user_cart.classList.add('no-view');
        user_cart_id.classList.toggle('no-view')
    }
})}

if(register_btn){
register_btn.addEventListener('click', ()=>{
    user_sign_in.classList.toggle('no-view')
    user_sign_up.classList.toggle('no-view')


})}

if(login_btn){
login_btn.addEventListener('click', ()=>{
    user_sign_up.classList.toggle('no-view')

    user_sign_in.classList.toggle('no-view')

})}



if(user_cart_button){
user_cart_button.addEventListener('click', ()=>{
    user_cart.classList.toggle('no-view');
    user_cart_id.classList.toggle('no-view');


    if(user_profile.classList.contains('no-view')){
       
    }
    else{
        user_profile.classList.add('no-view');
        user_profile_arrow_id.classList.toggle('no-view')
    }

   

})}



//ajax





