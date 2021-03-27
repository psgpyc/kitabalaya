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

    $('.book-modal-ajax-initial').hide()



    $('.featured-category-each').each(function (index, value) {
        if(index > 2){
            $(this).addClass('no-view')
        }

    })

    // Search Scroll Top

    $('#search-img').click(function (e) {
        $('html,body').animate({scrollTop:320}, 'slow')
        $('#searchbox').focus().keydown(function() {
          $('.search-result').show()


        });
    })

    $(document).on( 'scroll', function(e){

        if(scrollY > 500){
            $('.search').show()
            $('.search-result').hide()
            $('#searchbox').val('')


        }
        else {
            $('.search').hide()
        }



    });


    //hamburger button

    $("#hamburger-id").click(function (e) {
        $("#side-bar-id").removeClass('no-view')
        $("#close-side-bar-id").removeClass('no-view')
        $('body').css('overflow', 'hidden');
    })

    $("#close-side-bar-id").click(function (e) {
        $("#side-bar-id").addClass('no-view')
        $("#close-side-bar-id").addClass('no-view')
        $('body').css('overflow', 'auto');
    })

  // Start of Banner button click event

  $('.bannerbtn').each(function(btnIndex){

       $(this).click(function(){
           $(this).nextAll().removeClass('hover-style')
           $(this).prevAll().removeClass('hover-style')
           $(this).addClass('hover-style')

           $('.each-banner .banner').each(function (bnnrIndex) {
            if(btnIndex === bnnrIndex) {
                $('.each-banner').find('.banner-active').removeClass('banner-active').addClass('banner-off')
                $(this).addClass('banner-active').removeClass('banner-off')
            }
        })
       })
   })

    //end of banner button click event

    //Automatic transition of banner

    function getBannerClick(){
        let current = $('.each-banner img.banner-active')
        let currentBtn = $('.navigation-banner-button-wrapper button.hover-style')

        if(current.next().length !== 0){
            if(current.length === 0){
                $('.each-banner img:first-child').removeClass('banner-off').addClass('banner-active')
                $('#bb0').addClass('hover-style')
            }
            else {
                current.removeClass('banner-active').addClass('banner-off').next().addClass('banner-active').removeClass('banner-off')
                currentBtn.removeClass('hover-style').next().addClass('hover-style')

            }
        }
        else{
            $('.each-banner img:last-child').addClass('banner-off').removeClass('banner-active')
            $('.each-banner img:first-child').removeClass('banner-off').addClass('banner-active')
            $('.navigation-banner-button-wrapper button:last-child').removeClass('hover-style')
            $('.navigation-banner-button-wrapper button:first-child').addClass('hover-style')


        }
    }

    setInterval(getBannerClick, 20000)

    //end of automatic transition of the banner


      // Start Scroll on keypress : Search Form
      $( "#search-box-id" ).mousedown(function() {
          $('html,body').animate({scrollTop:320}, 'slow')
          searchResultBox = $('.search-result')
          $(this).keyup(function (e) {
              searchResultBox.show()
              // $(".search-button-wrapper").hide()
              let query = $(this).val()
              $.ajax({
                  headers: { "X-CSRFToken": $.cookie("csrftoken") },
                  url: '/home/ajax/search/',
                  method: 'POST',
                  mode: 'same-origin',
                  data: {
                    'query': query,
                  },

                  success: function (data) {
                      let searchResult = $('.search-result')
                     searchResult.children(".search-result-each").remove()
                     searchResult.children("p").remove()
                      if((data.data).length === 0){
                          $("<p>").addClass('search-result-each').html('Opps! Your choice is better than ours!!!!').insertBefore('.drop-result-button')
                      }
                    $.each(data.data, function (index,value) {
                        var searchPara = $("<p>")
                        searchPara.addClass('search-result-each').html(value).appendTo($(".search-result")).insertBefore(".drop-result-button")
                    })

                },


              })


              if($(this).val().length === 0){
                 searchResultBox.hide()
                  // $(".search-button-wrapper").show()
              }



          })



        });

    // Search Form Clear

    $("#clear-drop-result-button").click(function (e) {
        $("#search-box-id").val('')

    })

    //END

    $(document).click(function (e) {
        let container = $('.search-result')
        if(!container.is(e.target) && !$('#searchbox').is(e.target)){
           container.hide()
        }

    })


    // BOOK PRICE DETAIL BUTTONS




    // Book Category

    $(".side-bar-category-wrapper-main").each(function () {
        $(this).mouseenter(function (e) {
                $(this).children('.side-bar-category-details-wrapper').removeClass('no-view')
                $(this).children('.side-bar-category').children('.arrow-svg').removeClass('no-view')

        })

        $(this).mouseleave(function (e) {

            $(this).children('.side-bar-category-details-wrapper').addClass('no-view')
            $(this).children('.side-bar-category').children('.arrow-svg').addClass('no-view')

        })
    })


    //Rating

    // $('.fa').each(function(){
    //     $(this).mouseenter(function (e) {
    //         $(this).addClass('checked')
    //         $(this).prevAll('.fa').addClass('checked')
    //
    //
    //     })
    //
    //     $(this).mouseleave(function (e) {
    //         $(this).removeClass('checked')
    //         $(this).prevAll('.fa').removeClass('checked')
    //
    //
    //     })
    //
    //     $(this).click(function (e) {
    //         e.preventDefault();
    //         $(this).addClass('clicked-checked')
    //         $(this).prevAll('.fa').addClass('clicked-checked')
    //         $(this).nextAll('.fa').removeClass('clicked-checked')
    //         let ratingCount = (($(this).prevAll('.fa')).length)+1;
    //         let endPoint= '/home/rating/'+$("#book-slug").text()+'/'
    //          console.log(ratingCount)
    //
    //
    //         $.ajax({
    //             headers: { "X-CSRFToken": $.cookie("csrftoken") },
    //             url: endPoint,
    //             method: 'post',
    //             success: function (data) {
    //                 console.log(data.slug_name)
    //
    //             },
    //             data: {
    //                 'rating_count': ratingCount,
    //             }
    //
    //
    //
    //
    //             }
    //
    //         )
    //
    //     })
    //
    // })





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

    // BOOK BUY/RENT BUTTON DISPLAY

    // $('.dropdown').each(function(){
    //
    //     $(this).hover(function(e){
    //         $(this).children('.buy-rent-dropdown').removeClass('no-view')
    //
    //
    //
    //         },
    //         function (e) {
    //         $(this).children('.buy-rent-dropdown').addClass('no-view')
    //
    //
    //         })
    //
    //
    //
    // })


    // Restocked alert





    // DROP DOWN BOOK CARD

        $('.dropdown').each(function(){
            $(this).click(function(){
                let rent_buy_drop = $(this).children('.buy-rent-dropdown').toggleClass('no-view')

            })
        })


        $('.rent-buy-card').each(function () {
            $(this).click(function () {
                let changePriceList = $(this).parent().parent().parent().prev('.cat-style')

                let rentType = $(this).attr("name")
                let bookSlug = $(this).attr("value")
                let endPoint = 'ajax/get-book-price/'
                let method = 'GET'

                console.log(rentType)

                $.ajax({
                    url: endPoint,
                    type: method,
                    data: {
                        'bookSlug': bookSlug,
                        'rent-type': rentType,
                    },

                    success: function (res){
                        if(rentType === "buy-new"){
                            if(typeof res.rental_cost === 'undefined'){
                                changePriceList.text("OUT OF STOCK").css('color','red')


                            }

                            else if(res.in_stock_buy === 0){
                                changePriceList.text("OUT OF STOCK").css('color','red')


                            }


                            else{
                                changePriceList.text('NPR: ' + res.price).css('color','#3a3a3a')
                            }



                        }else{
                              if(typeof res.rental_cost === 'undefined' ){
                                changePriceList.text("OUT OF STOCK").css('color','red')


                            }else{
                            changePriceList.text('NPR: ' + res.rental_cost + '/day').css('color','#3a3a3a')
                        }}
                    }
                })


                $(this).insertBefore($(this).parent().prev('img'))
                ($(this).prev().insertBefore($(this).nextAll('.buy-rent-dropdown').children()))











            })


        })






    // PAGINATOR NEXT BUTON

    $('.arrow-right-next').each(function () {

        $(this).click(function () {

            let each_book = $('.featured-category-each')
            let scroll_range = each_book.length

            console.log(scroll_range)
            let view_start = each_book.not('.no-view').last().index()
            let no_view_start = view_start - 3

            if(view_start !== scroll_range) {
                each_book.eq(view_start).fadeIn(200, function () {
                    $(this).removeClass('no-view').css('display','flex')

                })
                each_book.eq(view_start+1).fadeIn(200, function () {
                    $(this).removeClass('no-view').css('display','flex')

                })
                each_book.eq(view_start+2).fadeIn(200, function () {
                    $(this).removeClass('no-view').css('display','flex')


                })


                each_book.eq(no_view_start).fadeOut(200, function () {
                    $(this).addClass('no-view')

                })
                each_book.eq(no_view_start+1).fadeOut(200, function () {
                    $(this).addClass('no-view')

                })
                each_book.eq(no_view_start+2).fadeOut(200, function () {
                    $(this).addClass('no-view')
                })
            }

        })

    })


    $('.arrow-left-next').each(function(){

        $(this).click(function(){
            let each_book = $('.featured-category-each')
            let view_start_index = (each_book.not('.no-view').first().index()-1)
            if(view_start_index === 0){
                let view_start = 0
                let view_end = 0
            }
            else{
                let view_end = view_start_index

                 each_book.eq(view_start_index-1).fadeIn(200, function () {
                    $(this).removeClass('no-view').css('display','flex')


                })

                 each_book.eq(view_start_index-2).fadeIn(200, function () {
                    $(this).removeClass('no-view').css('display','flex')


                })

                 each_book.eq(view_start_index-3).fadeIn(200, function () {
                    $(this).removeClass('no-view').css('display','flex')


                })


                each_book.eq(view_end).fadeOut(200, function () {
                    $(this).addClass('no-view')

                })
                 each_book.eq(view_end+1).fadeOut(200, function () {
                    $(this).addClass('no-view')

                })
                 each_book.eq(view_end+2).fadeOut(200, function () {
                    $(this).addClass('no-view')

                })

            }
        })
    })





    //   $(".rent-link").each(function(){
    //       $(this).click(function(e){
    //           e.preventDefault();
    //
    //           let endPoint = $(this).attr('href')
    //           console.log(endPoint)
    //
    //            $.ajax({
    //                url: endPoint,
    //                beforeSend: function() {
    //                        $("#the-book-modal-id").fadeIn();
    //                        $(".loading-div").show()
    //
    //                        $("#book-title-id").text("Loading...")
    //                        $("#book-author-id").text("Loading...")
    //                        $("#book-img-id").hide()
    //                        $("#book-summary").text("Loading...")
    //                        $("#book-condition-span-id").text("Loading...")
    //                        $("#book-quality-rating-span-id").text("Loading...")
    //                        $("#book-slug").text("Loading...")
    //                        $("#published-date-id").text("Loading...")
    //                        $("#page-count-id").text("Loading...")
    //                        $('#book-genre-span-id').text("Loading...")
    //                        $('#book-rating-id').text("Loading...")
    //
    //                },
    //
    //                success: function(data) {
    //                    if(data.book){
    //                        $("#the-book-modal-id").fadeIn();
    //
    //                        $("#book-title-id").text(data.book.title)
    //                        $("#book-author-id").text(data.book.author)
    //                        $(".loading-div").hide()
    //                        $("#book-img-id").attr('src', data.book.image).show()
    //                        $("#book-summary").text(data.book.summary)
    //                        $("#book-condition-span-id").text(data.book.book_condition)
    //                        $("#book-quality-rating-span-id").text(data.book.quality_rating)
    //                        $("#book-slug").text(data.book.slug)
    //                        $("#published-date-id").text(data.book.published_date)
    //                        $("#page-count-id").text(data.book.page_count)
    //                        $('#book-genre-span-id').text(data.book.book_genre)
    //                        $('#book-rating-id').text(data.book.book_rating)
    //                        let count = 0
    //                        $(".fa").each(function (e) {
    //
    //                            if(count <= data.book.book_rating){
    //                                $(this).addClass('clicked-checked')
    //                                count++;
    //
    //                            }
    //
    //
    //                        })
    //
    //
    //                        $('body').css('overflow', 'hidden');
    //
    //
    //
    //
    //
    //
    //                    }
    //
    //
    //                }
    //
    //            }
    //
    //
    //
    //
    //
    //
    //            )
    //
    //       });
    // });
    //
    // $("#close-book-modal-id").click(function(e){
    //
    //     $('#the-book-modal-id').hide();
    //     $('#book-img-id').attr('src','')
    //     $('.fa').each(function (){
    //         $(this).prevAll('.fa').removeClass('clicked-checked')
    //         $(this).removeClass('clicked-checked')
    //         $(this).nextAll('.fa').removeClass('clicked-checked')
    //     })
    //     $('body').css('overflow', 'auto');
    //
    //
    //
    // })



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
                    // window.location.href = 'http://kitabalaya.com:8000/home/'
                    window.location.href = 'https://www.kitabalaya.com/home/'

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





