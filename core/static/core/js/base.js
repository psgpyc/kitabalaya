
$(document).ready(function(){




    $('body').show()




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

    $('#search-svg').click(function (e) {
        $('html,body').animate({scrollTop:320}, 'slow')
        $('#search-box-id').focus().keydown(function() {
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

    //User-cart button

    $('#close-user-cart-btn').click(function (e) {
        $('.user-cart-wrapper').addClass('no-view')

    })


    //hamburger button

    $("#hamburger-id").click(function (e) {
        $("#side-bar-id").removeClass('no-view')
        $("#close-side-bar-id").removeClass('no-view')
        alert(e.target())

        $('body').css('overflow', 'hidden');
    })

    $("#close-side-bar-id").click(function (e) {
        $("#side-bar-id").addClass('no-view')
        $("#close-side-bar-id").addClass('no-view')
        $('body').css('overflow', 'auto');
    })

  //  Banner Auto
  //   var currentSlide = 1

  //   var delayVal = 1000
  //   var finalTimeOut = 3000
  //
  //
  //
  //

  //
  //
  //   var interval
  //
  //   function startSlider(){
  //       interval = setInterval(function() {
  //       bannerWrap.animate({
  //           marginLeft : '-=100%',
  //       }, 1000, function () {
  //           currentSlide++;
  //           console.log('auto' + currentSlide)
  //           if( currentSlide === slideCount){
  //               currentSlide = 1
  //               $(this).css('margin-left', '0%');
  //           }
  //       } );
  //   }, finalTimeOut)
  //   }
  //
  //   function pauseSlider(){
  //       clearInterval(interval)
  //
  //   }
  //
  //   $('.banner').on('mouseenter', pauseSlider).on('mouseleave', startSlider)
  //   startSlider()


    // Banner slide btn
    // var slideScore = 1
    // var currentSlide = 1
    // var bannerWrap = $('.each-banner')
    //     slideCount = bannerWrap.children().length
    //     widthLength = slideCount*100 + '%'
    //
    //
    // bannerWrap.css('width', widthLength)

    var active_banner
    var next_banner

    var prev_banner
    var bannerWrapper =  $('.banner-collection')

    var bannerChildLength = bannerWrapper.children().length
    activeBannerCount = 1

    function get_active_banner(){
        if(activeBannerCount < bannerChildLength){
            current_banner = bannerWrapper.find('.banner-active')
            if (current_banner.length === 1){
                return current_banner

            }
        }
        else{
            return 0
        }
    }


    $("#next-banner-btn").on('click', function(){
        active_banner = get_active_banner()
        if( active_banner !== 0){

            next_banner = active_banner.next()
            active_banner.removeClass('banner-active')
            next_banner.addClass('banner-active')
            activeBannerCount++





        }
        if(active_banner === 0){
            bannerWrapper.find('.banner-active').removeClass('banner-active')
            bannerWrapper.children().first().addClass('banner-active')
            activeBannerCount = 1

        }
    })


    $("#prev-banner-btn").on('click', function () {
        if(activeBannerCount === 1){
            bannerWrapper.find('.banner-active').removeClass('banner-active')
            bannerWrapper.children().last().addClass('banner-active')
            activeBannerCount = bannerChildLength


        }
        else{
            activeBannerCount--

        active_banner = get_active_banner()
        if(active_banner !== 0){
            prev_banner = active_banner.prev()
            active_banner.removeClass('banner-active')
            prev_banner.addClass('banner-active')

        }

        }



    })

    var interval;

    function autoSlider(){
        interval = setInterval(function () {
            active_banner = get_active_banner()
            if(active_banner !== 0 ){
                next_banner = active_banner.next()
                active_banner.removeClass('banner-active')
                next_banner.addClass('banner-active')
                activeBannerCount++

            }

            if(active_banner === 0){
                bannerWrapper.find('.banner-active').removeClass('banner-active')
                bannerWrapper.children().first().addClass('banner-active')
                activeBannerCount = 1
                console.log(activeBannerCount)

            }







    }, 4000)

    }

    function pauseSlider(){
        clearInterval(interval)

    }

    bannerWrapper.on('mouseenter', pauseSlider).on('mouseleave', autoSlider)
    $('#prev-banner-btn').on('mouseenter', pauseSlider).on('mouseleave', autoSlider)
    $('#next-banner-btn').on('mouseenter', pauseSlider).on('mouseleave', autoSlider)

    autoSlider()





    // Start Scroll on keypress : Search Form
    $( "#search-box-id" ).focus(function() {
          $('html,body').animate({scrollTop:420}, 'slow')
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



    // BOOK CArd Rental Button


    // $('.rental-button').each(function(){
    //     $(this).click(function (event) {
    //         event.preventDefault()
    //         $('.rental-popup-wrapper').removeClass('no-view')
    //         $('body').css('overflow', 'hidden');
    //         $('.main-content-wrapper').addClass('toggle-display-body')
    //         $('.newsletter').addClass('toggle-display-body')
    //         $('.banner-wrapper').addClass('toggle-display-body')
    //
    //
    //         let slugBook = $(this).attr('name')
    //
    //         let title = slugBook.split('?')[0]
    //         let rental = slugBook.split('?')[1].split('.')[0]
    //         let deposit = slugBook.split('?')[2].split('.')[0]
    //
    //         $('#title-id').text(title)
    //         $('#rental').text('Rental Charge:   रु.' + deposit+'/day')
    //         $('#depo').text('Refundable Security Deposit:  रु.' + rental )
    //
    //
    //
    //
    //
    //
    //
    //
    //     })
    // })



    //Close Rent Pop Up

    $('.rental-button').each(function () {
        $(this).click(function () {
            $(this).parent().parent().prev('.rental-popup-wrapper').removeClass('no-view')
            $('body').css('overflow', 'hidden');

        })

    })


    $('.close-btn > img').click(function(){
        $(this).parent().parent().addClass('no-view')
            $('body').css('overflow', 'auto');
            $('.main-content-wrapper').removeClass('toggle-display-body')
            $('.newsletter').removeClass('toggle-display-body')
            $('.banner-wrapper').removeClass('toggle-display-body')


    })


    $('.faqbtn').each(function () {
        $(this).click(function () {
            $('.faqsp').toggleClass('no-view')


        })

    })

    $('.faqbtnone').each(function () {
        $(this).click(function () {
            $('.faqspone').toggleClass('no-view')


        })

    })





    // $(document).click(function(e){
    //     let container = $('.rental-popup-wrapper')
    //
    //      if(!container.is(e.target) && container.has(e.target).length === 0){
    //          container.hide();
    //      }
    //
    //
    // })





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

                console.log(rentType)
                let endPoint = 'ajax/get-book-price/'
                let method = 'GET'


                $.ajax({
                    url: '/home/ajax/get-book-price',
                    type: method,
                    data: {
                        'bookSlug': bookSlug,
                        'rent-type': rentType,
                    },

                    error: function (error){
                        console.log(error)
                    },


                    success: function (res){
                        if(rentType === "buy-new"){
                            if(typeof res.price === 'undefined'){
                                changePriceList.text("OUT OF STOCK").css('color','red')


                            }

                            else if(res.in_stock_buy === 0){
                                changePriceList.text("OUT OF STOCK").css('color','red')


                            }


                            else{
                                changePriceList.text('NPR: ' + res.price).css('color','#3a3a3a')
                            }



                        }else{
                              if(typeof res.price === 'undefined' ){
                                changePriceList.text("OUT OF STOCK").css('color','red')


                            }else{
                            changePriceList.text('NPR: ' + res.price + '/day').css('color','#3a3a3a')
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
                each_book.eq(view_start).fadeIn(300, function () {
                    $(this).removeClass('no-view').css('display','flex')

                })
                each_book.eq(view_start+1).fadeIn(300, function () {
                    $(this).removeClass('no-view').css('display','flex')

                })
                each_book.eq(view_start+2).fadeIn(300, function () {
                    $(this).removeClass('no-view').css('display','flex')


                })


                each_book.eq(no_view_start).fadeOut(300, function () {
                    $(this).addClass('no-view')

                })
                each_book.eq(no_view_start+1).fadeOut(300, function () {
                    $(this).addClass('no-view')

                })
                each_book.eq(no_view_start+2).fadeOut(300, function () {
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

function getLangChecked(){
        return  $('.category-lang-wrap form input:checked').val()

    }

// function getPriceFilterChecked(){
//         return $('.category-price-wrap form input:checked').val()
// }

function getGenSortChecked(){
        return $('.category-gen-sort-wrap form input:checked').val()
}

function getSubGenreChecked(){
        return $('.category-genre-wrap form input:checked').val()

}

$('.category-genre-wrap  .each-category-genre').on('click', function () {
    let genreVal = getSubGenreChecked()
    let langVal = getLangChecked()
    // let priceVal =  getPriceFilterChecked()
    let sortVal =  getGenSortChecked()


    $(this).prevAll().find('input:checkbox').prop('checked', false)
    $(this).nextAll().find('input:checkbox').prop('checked', false)

    let endPoint = $(this).attr('action')
    let genreData = $(this).attr('data-genre-slug')
    let httpMethod = $(this).attr('method')
    let dataVal = {
         'genre': genreVal,
        'lang': langVal,
        // 'price': priceVal,
        'sort': sortVal,
    }




   $.ajax({
       headers: { "X-CSRFToken": $.cookie("csrftoken") },
       url: endPoint,
       data : dataVal,
       mode: 'same-origin',

       success: function(data){


       }
   })


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



// ADD PRODUCT PURCHASE FORM

cartProductWrapClone = $('#cart-product-wrapper-clone')
let topCartDisplay =$('.top-cart-display')


var loaded = false
let cart_length = 0





$('.add-product-btn-form').on('click', function (e) {
    e.preventDefault()
    let productAddBtn= $(this)
    let productId = productAddBtn.attr('data-product-slug')
    let orderType = productAddBtn.attr('data-order-type')
    let endPoint = productAddBtn.attr('action')
    let httpMethod = productAddBtn.attr('method')
    let data = {
        'productSlug': productId,
        'orderType': orderType,
    }
    let btnSelect = $(this)





    $.ajax({
            headers: { "X-CSRFToken": $.cookie("csrftoken") },
            url: endPoint,
            method: httpMethod,
            data: data,
            mode: 'same-origin',


            beforeSend: function() {
                alert(endPoint)
                btnSelect.find('.buy-btn').text('Adding to Cart.')


            },



            success: function(successData){
                if(successData.created){
                    if(successData.created === 'true'){
                        if(successData.book['cart_product_count'] > 0){
                            $('.empty-cart').addClass('no-view')
                            topCartDisplay.removeClass('no-view')
                            $('#cart-item-count').text('('+ successData.book['cart_product_count']+')')

                             let cartProductWrap =cartProductWrapClone.clone()

                            cartProductWrap.find('.book-title').text(successData.book['title'])
                            cartProductWrap.find('.book-author-name').text(successData.book['author_name'])
                            cartProductWrap.find('.cart-cost-display').text('रु. '+ successData.book['mrp_price'] + ' *  ' + successData.book['quantity'])
                            cartProductWrap.find('.book-image').attr('src', successData.book['book_image'] )

                            cartProductWrap.find('.cart-item-remove').attr('data-order-type',successData.book['rent_or_buy'])
                            cartProductWrap.find('.cart-item-remove').attr('data-order-slug',successData.book['book_slug'])

                            if(successData.book['rent_or_buy'] === 'RNT') {
                                cartProductWrap.find('.rent-buy-option').text('for RENT')

                            }else{
                                cartProductWrap.find('.rent-buy-option').text('for PURCHASE')


                            }
                            cartProductWrap.attr('id', successData.book['book_slug'] +'-'+successData.book['rent_or_buy'])
                            // imgSrc = successData.book['book_image']

                            topCartDisplay.append(cartProductWrap.removeClass('no-view'))


                            $('.cart-added-display').addClass('cart-added-display-show')

                            setTimeout(function() {
                                $('.cart-added-display').removeClass('cart-added-display-show')


                            }, 1000); // <-- time in milliseconds




                        }
                        if(successData.book['cart_product_count'] === 0){
                            $('.empty-cart').removeClass('no-view')
                            topCartDisplay.addClass('no-view')

                        }

                }
                }

                if(successData.created === 'false'){
                    let book_slug = successData.cart_item['slug']
                    let book_quantity = successData.cart_item['quantity']
                    let order_type = successData.cart_item['rent_or_buy']
                    $('#cart-item-count').text('('+ successData.cart_item['cart_product_count']+')')

                    $('#'+book_slug+'-'+order_type ).find('.cart-cost-display').text('रु. '+ successData.cart_item['mrp_price'] + ' *  ' + book_quantity)

                    $('.cart-added-display').addClass('cart-added-display-show')

                            setTimeout(function() {
                                $('.cart-added-display').removeClass('cart-added-display-show')


                            }, 500); // <-- time in milliseconds
                }

                if(successData.created === 'Rent False'){
                    alert('You can only rent a single copy of a book')
                }

                btnSelect.find('.buy-btn').text('BUY')









                cart_length = topCartDisplay.children().length







            },
            error: function(errorData){
                console.log("error")
                console.log(errorData)
                alert('fucked')
            }
        })




})

// REMOVE CART ITEM



$(document).on('click', '.cart-item-remove', function (event) {
    event.preventDefault()
    let cart_item = $(this).parent()
    let orderType = $(this).attr('data-order-type')
    let book_slug = $(this).attr('data-order-slug')
    let endPoint = $(this).attr('action')
    let httpMethod = $(this).attr('method')

    let data = {
        'book_slug': book_slug,
        'orderType': orderType,
    }

    $.ajax({
        headers: { "X-CSRFToken": $.cookie("csrftoken") },
        url: endPoint ,
        method: httpMethod,
        data: data,
        mode: 'same-origin',

        success: function(successData){


            if(successData['data'] === 'success'){
                cart_item.remove()
                 $('#cart-item-count').text('('+successData['cart_product_count']+')')

            }

            if(topCartDisplay.children().length === 1){
                $('.empty-cart').removeClass('no-view')
                topCartDisplay.addClass('no-view')
                $('.cart-submit-button').addClass('no-view')
                $('#cart-item-count').text('('+0+')')


            }


        },
        error: function(errorData){
                console.log("error")
                console.log(errorData)
                alert('fucked')
            }




    })


})


































let search_button = document.getElementById('search-img')
let search_end = document.getElementById('search-end')
let search_box = document.getElementById('searchbox')
let secondary_nav_book_list_category = document.getElementById('book-list-category-id')
let banner_wrapper = document.getElementById('banner-img-id')

let hamburger = document.getElementById('hamburger-id');
let side_bar = document.getElementById('side-bar-id');





const user_sign_in = document.getElementById('user-sign-in-wrapper-id');
const user_sign_up = document.getElementById('user-sign-up-wrapper-id');






const register_btn = document.getElementById('user-register')
const  user_register = document.getElementById('user-profile-register-wrapper-id')
const  login_btn = document.getElementById('user-login')



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



let user_cart = $('#user-cart-wrapper-id')
let user_cart_button = $('#cart-id')
let user_cart_id = $('#arrow-cart-id')
let user_profile = $('#user-profile-wrapper-id')
let user_profile_arrow_id = $('#arrow-id')
let user_profile_button = $('#accounts-id')
var empty_cart = $('.empty-cart')



if(user_cart_button) {
    user_cart_button.on('click', function () {
        $('#user-cart-wrapper-id').toggleClass('no-view')
        $('#arrow-cart-id').toggleClass('no-view')


        if (user_profile.hasClass('no-view')) {
        } else {
            user_profile.addClass('no-view')
            user_profile_arrow_id.toggleClass('no-view')
        }




        if(loaded === false){
            $.ajax({
            url: '/cart/display/',



            success: function(response){
                if(response.cart_obj === 0){
                    $('.empty-cart').removeClass('no-view')
                    topCartDisplay.addClass('no-view')

                    loaded = true



                }
                else{
                    loaded = true

                    topCartDisplay.removeClass('no-view')
                    $('.cart-submit-button').removeClass('no-view')

                    topCartDisplay.children('.cart-product' +
                        '-wrapper:not(:first-child)').remove()

                    $.each(response.data, function(key, value){

                        let cartProductWrap =cartProductWrapClone.clone()

                        cartProductWrap.find('.book-title').text(value['title'])
                        cartProductWrap.find('.book-author-name').text(value['author_name'])
                        cartProductWrap.find('.cart-cost-display').text('रु. '+ value['mrp_price'] + ' *  ' + value['quantity'])
                        cartProductWrap.find('.book-image').attr('src', value['img_url'] )
                        cartProductWrap.attr('id', value['slug'] +'-'+value['rent_or_buy'])

                        cartProductWrap.find('.cart-item-remove').attr('data-order-type',value['rent_or_buy'])
                        cartProductWrap.find('.cart-item-remove').attr('data-order-slug',value['slug'])


                         if(value['rent_or_buy'] === 'RNT') {
                                cartProductWrap.find('.rent-buy-option').text('for RENT')

                            }else{
                                cartProductWrap.find('.rent-buy-option').text('for PURCHASE')


                            }

                        topCartDisplay.append(cartProductWrap.removeClass('no-view'))
                    })

                    cart_length = topCartDisplay.children().length




                }

            }






        })

        }



    })
}


if(user_profile_button){
user_profile_button.on('click', function () {
    user_profile.toggleClass('no-view')
    user_profile_arrow_id.toggleClass('no-view')

    if(user_cart.hasClass('no-view')){}
    else{
        user_cart.addClass('no-view')
        user_cart_id.toggleClass('no-view')

    }


})}

//ajax





