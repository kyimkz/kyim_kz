// ########################################################## ADD REVIEW ####################################################################
//дописать месяцы
const months = ["Jan", "Feb","March", "April", "May", "June", 
"July", "Aug", "Sept", "Oct", "Nov", "Dec"];

$("#commentForm").submit(function(e){
    e.preventDefault();

    let dt = new Date();
    let time = dt.getDay() + " " + months[dt.getUTCMonth()] + ", " + dt.getFullYear()

    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: "json",
        success: function(response){
            console.log("Review saved to Database");

            if(response.bool == true){
                $("#reviewFinal").html("Review added!")
                $(".hide-comment-form").hide()
                $(".add-review-here").hide()

                // расположить див с начала лупа до его конца(не включая луп)
                // let _html = '<div>'
                //     _html += '<img src = "https://t3.ftcdn.net/jpg/03/58/90/78/360_F_358907879_Vdu96gF4XVhjCZxN2kCG0THTsSQi8IhT.jpg" width="200" height="200" alt ="" />'
                //     _html += '<a href = "#" class= "font-heading text-brand">' + response.context.user + '</a> &nbsp;'        
                //     _html += '<div>'
                //     _html += '<div>'
                //     _html += '<span>' + time + '</span>'
                //     _html += '</div>'

                //     for(let i =1; i<=response.context.rating; i++){

                //         _html += '<i class = "fas fa-star text-warning"></i>'
                //     }

                //     _html += '</div>'
                //     _html += '<p>'+ response.context.review + '</p>'
                //     _html += '</div>'
                //     $(".comment-list").prepend(_html)

                let _html = '<div class="comment">'
                    _html += '<img src="' + response.context.user.profile_image_url + '" style="width: 70px; height: 70px; border-radius: 50%; object-fit: cover; border-radius: 50%" alt="My image" id="img" />&nbsp;&nbsp;'
                    _html += '<div class="column">'
                    _html += '<div class="smth">'
                    _html += '<span class= "font-heading text-brand">' + response.context.user.username + '</span>'
                    _html += '</div>'
                    _html += '<div class="smth">'
                    _html += '<span>' + time + '</span>'
                    _html += '</div>'
                    _html += '<div class="smth">'

                    for(let i =1; i<=response.context.rating; i++){

                        _html += '<i class = "fas fa-star text-warning"></i>'
                    }

                    _html += '</div>'
                    _html += '<p class="smth">'+ response.context.review + '</p>'
                    _html += '</div>'
                    _html += '</div>'
                    $(".comment-list").prepend(_html)
            }
            // работа для comment-list
            

        }
    })
})

// ########################################################### FILTER FUNCTION ###############################################################

$(document).ready(function () {
    $(".filter-checkbox, #price-filter").on("click", function(){
        console.log("A checkbox have been clicked");
    
        let filter_object = {}

        let min_price = $('#max_price').attr("min")
        let max_price = $('#max_price').val()

        filter_object.min_price = min_price;
        filter_object.max_price = max_price;

        $(".filter-checkbox").each(function() {
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function(element){
                return element.value
            })
        }) 
        console.log("Filter Object is: ", filter_object);
        $.ajax({
            url: '/filter-products',
            data: filter_object, 
            dataType: 'json',
            beforeSend: function() {
                console.log("Trying to filter product...");
            },
            success: function(response) {
                console.log(response);
                console.log("Data filtered successfully...");
            $("#filtered-product").html(response.data)
            }
        })
    })
    $("#max_price").on("blur", function(){
        let min_price = $(this).attr("min")
        let max_price = $(this).attr("max")
        let current_price = $(this).val()

        if(current_price < parseInt(min_price) || current_price > parseInt(max_price)){
            alert("Price must between " + min_price + 'tg and ' + max_price + 'tg')
            $(this).val(min_price)
            $('#range').val(min_price)

            $(this).focus()

            return false
        }
    })
})

// ############################################################ ADD TO CART ##################################################################

$(document).on("click", ".add-to-cart-btn", function(){
    let this_val = $(this);
    let index_val = this_val.attr("data-index");
    let quantity = $(".product-quantity-" + index_val).val();
    let product_title = $(".product-title-" + index_val).val();
    let product_id = $(".product-id-"+ index_val).val();
    let product_price = $(".product-current-price-"+ index_val).text();
    let product_pid = $(".product-pid-"+ index_val).val();
    let product_image = $(".product-image-" + index_val).val();
    let product_size = $(".product-size-" + index_val).val(); // Get selected size

     // If size is undefined, set it to 'S'
     if (!product_size) {
        product_size = 'S';
    }

    console.log("Quantity: ", quantity);
    console.log("Title: ", product_title);
    console.log("Price: ", product_price);
    console.log("ID: ", product_id);
    console.log("Pid: ", product_pid);
    console.log("Image: ", product_image);
    console.log("Size: ", product_size); // Log selected size

    $.ajax({
        url: '/add-to-cart',
        data: {
            'id': product_id,
            'pid': product_pid,
            'image': product_image,
            'quantity': quantity,
            'title': product_title,
            'price': product_price,
            'size': product_size // Include selected size in data
        },
        dataType: 'json',
        beforeSend: function(){
            console.log("Adding product...");
        },
        success: function(response){
            this_val.html('<i class="fa-solid fa-cart-plus" style="color: pink;"></i>');
            console.log("Successfully added product");

            $(".cart-items-count").text(response.totalItemsInCart);
        }
    });
});

    

// ############################################################ UPDATE CART ##################################################################

$(document).ready(function() {
    // Event delegation for quantity update button
    $(document).on("click", ".update-item", function(){
        let product_id = $(this).data("product");
        let product_quantity = $(".product-quantity-"+ product_id).val();
        let product_size = $("#product-size-"+ product_id).val(); // Get the selected size
                
        console.log("Product ID:", product_id);
        console.log("Quantity:", product_quantity);
        console.log("Size:", product_size);
                
        $.ajax({
            url: "/update-cart",
            data: {
                "id": product_id,
                "quantity": product_quantity,
                "size": product_size, // Include the selected size in the data
            },
            dataType: "json",
            beforeSend: function() {
                // Hide or disable any loading indicators/buttons if needed
            },
            success: function(response){
                // Update cart total and items count
                $(".text-body").text("Total cart items: " + response.totalItemsInCart);
                $(".cart-items-count").text(response.totalItemsInCart);
                
                // Replace cart content with updated data
                $("#cart-list").html(response.data);
                
                console.log("Cart updated successfully.");
            },
            error: function(xhr, status, error) {
                console.error("Error updating cart:", error);
            }
        });
    });
});
 
 
 // ############################################################ DELETE CART ##################################################################

 $(document).ready(function() {
    $(document).on("click", ".delete-item", function(){
        let product_id = $(this).attr("data-product")
        let this_val = $(this)

        console.log("Item ID: ", product_id);

        $.ajax({
            url: "/delete-from-cart",
            data: {
                "id": product_id
            },
            dataType: "json",
            beforeSend: function(){
                this_val.hide()
            },
            success: function(response){
                this_val.show()
                $(".cart-items-count").text(response.totalItemsInCart)
                $("#cart-list").html(response.data)
            }
        })
    })
})

// ############################################################  ADD TO WISHLIST ##################################################################

function updateWishlistCount() {
    $.ajax({
        url: "/get-wishlist-count/",
        dataType: "json",
        success: function(response) {
            $(".wishlist-items-count").text(response.wishlist_count);
        },
        error: function(xhr, status, error) {
            console.error("Error fetching wishlist count:", error);
        }
    });
}

updateWishlistCount();

function updateAddToWishlistButton(product_id, addButton) {
    $.ajax({
        url: "/check-product-in-wishlist/",
        data: {
            "id": product_id
        },
        dataType: "json",
        success: function(response) {
            if (response.in_wishlist) {
                addButton.find("i").removeClass("fa-regular").addClass("fa-solid").css("color", "pink");
            }
        },
        error: function(xhr, status, error) {
            console.error("Error checking wishlist status:", error);
        }
    });
}

function addToWishlist(product_id, addButton) {
    $.ajax({
        url: "/add-to-wishlist",
        data: {
            "id": product_id
        },
        dataType: "json",
        beforeSend: function(){
            console.log("Adding product to wishlist");
        },
        success: function(response){
            if(response.bool === true){
                console.log("Success");
                addButton.find("i").removeClass("fa-regular").addClass("fa-solid").css("color", "pink");
                updateWishlistCount();
            }
        },
        error: function(xhr, status, error) {
            console.error("Error adding product to wishlist:", error);
        }
    });
}

function removeFromWishlist(wishlist_id, removeButton) {
    $.ajax({
        url: "/remove-from-wishlist",
        data:{
            "id": wishlist_id
        },
        dataType: "json",
        beforeSend: function(){
            removeButton.hide();
            console.log("Deleting from wishlist");
        },
        success: function(response){
            removeButton.show();
            $("#wishlist-list").html(response.data);
            updateWishlistCount();
        },
        error: function(xhr, status, error) {
            console.error("Error removing product from wishlist:", error);
        }
    });
}

$(document).on("click", ".add-to-wishlist", function(){
    let product_id = $(this).attr("data-product-item");
    let addButton = $(this);
    addToWishlist(product_id, addButton);
});

$(".add-to-wishlist").each(function() {
    let product_id = $(this).attr("data-product-item");
    let addButton = $(this);
    updateAddToWishlistButton(product_id, addButton);
});

$(document).on("click", ".delete-wishlist-product", function(){
    let wishlist_id = $(this).attr("data-wishlist-product");
    let removeButton = $(this);
    console.log("wishlist_id: ", wishlist_id);
    removeFromWishlist(wishlist_id, removeButton);
});


$(document).on("click", ".default-address", function(){
    let id = $(this).attr("data-address-id");
    let this_val = $(this);
    console.log("ID id:", id);
    console.log("ID id:", this_val);
})



/*$(".add-to-cart-btn").on("click", function(){
    let quantity = $("#product-quantity").val()
    let product_title = $(".product-title").val()
    let product_id = $(".product-id").val()
    let product_price  = $ (".product-current-price").text()
    let this_val =$(this)

    console.log("Quantity: ", quantity);
    console.log("Title: ", product_title);
    console.log("Price: ", product_price);
    console.log("ID: ", product_id);
    console.log("Quantity: ", this_val);

    $.ajax({
        url: '/add-to-cart',
        data: {
            'id':product_id,
            'quantity': quantity,
            'title': product_title,
            'price':product_price,
        },
        dataType: 'json',
        beforeSend: function(){
            console.log("Adding product...");
        },
        success: function(response){
            this_val.html("Item added to cart")
            console.log("Successfully added product");

            $(".cart-items-count").text(response.totalItemsInCart)
        }
    })

})
//add to cart*/