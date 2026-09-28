// =====================================
// ELEMENTS
// =====================================

const productsContainer =                           //document: represents your HTML webpage.
    document.getElementById("products");           //getElementById:Find the HTML element whose id is "products".
                                                   //const :  creates a variable whose reference cannot be reassigned.
const searchInput =                                //productsContainer : const creates a variable whose reference cannot be reassigned.
    document.getElementById("searchInput");        //Find the HTML element with ID products and store it in a JavaScript variable called productsContainer

const productForm =
    document.getElementById("productForm");

const formMessage =
    document.getElementById("formMessage");

const noResults =
    document.getElementById("noResults");

const banner =
    document.getElementById("banner");

const loading =
    document.getElementById("loading");


// =====================================
// STORE PRODUCTS
// =====================================

let allProducts = [];


// =====================================
// SHOW LOADING
// =====================================

function showLoading() {

    loading.classList.remove("hidden");

}


// =====================================
// HIDE LOADING
// =====================================

function hideLoading() {

    loading.classList.add("hidden");

}


// =====================================
// SHOW SUCCESS / ERROR BANNER
// =====================================

function showBanner(message, type) {

    const banner = document.getElementById("banner");

    banner.textContent = message;

   if (type === "success") {
        banner.className =
            "block p-3 my-3 rounded-lg font-semibold bg-green-100 text-green-700";
    } else {
        banner.className =
            "block p-3 my-3 rounded-lg font-semibold bg-red-100 text-red-700";
    }

    setTimeout(() => {
        banner.className = "hidden";
    }, 3000);
}


// =====================================
// GET PRODUCTS
// =====================================

async function loadProducts() {

    showLoading();

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/products"
        );


        if (!response.ok) {

            throw new Error(
                "Failed to load products"
            );

        }


        allProducts =
            await response.json();


        console.log(
            "Products received:",
            allProducts
        );


        displayProducts(allProducts);


    } catch (error) {

        console.error(error);


        showBanner(
            "Failed to load products",
            "error"
        );


    } finally {

        hideLoading();

    }

}


// =====================================
// DISPLAY PRODUCTS
// =====================================

function displayProducts(products) {

    // Clear old cards
    productsContainer.innerHTML = "";   //The HTML content inside an element.


    // No products
    if (products.length === 0) {

        noResults.classList.remove("hidden");

        return;

    }


    noResults.classList.add("hidden");


    // Create each product card
    products.forEach(product => {

        const card =
            document.createElement("div");   //JavaScript creates a new <div> element that you can use as your product card.


        card.className =
            "bg-white rounded-xl p-4 shadow-sm " +
            "hover:shadow-lg transition duration-200";


        // =====================================
        // CARD HTML
        // =====================================

        card.innerHTML = `

            <!-- Product Image -->

            <div
                class="h-44 bg-gray-100 rounded-lg
                       flex items-center justify-center"
            >

                <div
                    class="text-gray-400 text-lg"
                >
                    ${product.title}
                </div>

            </div>


            <!-- Product Title -->

            <h2 class="text-xl font-bold mt-4">
                ${product.title}
            </h2>


            <!-- Category -->

            <span
                class="inline-block mt-2 px-3 py-1
                       rounded-full bg-blue-100 text-blue-600
                       text-sm font-semibold"
            >
                ${product.category}
            </span>


            <!-- Price -->

            <div class="mt-4">

                <span class="text-2xl font-bold">
                    ₹${product.price}
                </span>


                <span class="ml-2 text-slate-400">
                    ($${(product.price / 83).toFixed(2)})
                </span>

            </div>


            <!-- Stock -->

            <div class="mt-4 flex items-center gap-2">

                <span class="text-green-600 text-xl">
                    📦
                </span>


                <span class="text-slate-600">
                    Stock: ${product.stock}
                </span>

            </div>


            <!-- ================================= -->
            <!-- BUY NOW BUTTON -->
            <!-- ================================= -->

            <button
                class="buy-btn"
                onclick="buyNow(${product.id})"
                ${product.stock <= 0 ? "disabled" : ""}
            >

                ${
                    product.stock <= 0
                        ? "Out of Stock"
                        : "Buy Now"
                }

            </button>

        `;


        // Add card to page
        productsContainer.appendChild(card);

    });

}


// =====================================
// SEARCH
// =====================================

searchInput.addEventListener(
    "input",
    function () {

        const text =
            searchInput.value
                .toLowerCase()
                .trim();


        const filteredProducts =
            allProducts.filter(product =>

                product.title
                    .toLowerCase()
                    .includes(text)

                ||

                product.category
                    .toLowerCase()
                    .includes(text)

            );


        displayProducts(filteredProducts);

    }
);


// =====================================
// CREATE PRODUCT
// =====================================

productForm.addEventListener(
    "submit",
    async function (event) {

        // Stop page refresh
        event.preventDefault();


        // Get form values
        const product = {

            title:
                document
                    .getElementById("title")
                    .value,


            category:
                document
                    .getElementById("category")
                    .value,


            price:
                parseFloat(
                    document
                        .getElementById("price")
                        .value
                ),


            stock:
                parseInt(
                    document
                        .getElementById("stock")
                        .value
                )

        };


        showLoading();


        try {

            // POST /products

            const response =
                await fetch(
                    "http://127.0.0.1:8000/products",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(product)
                    }
                );


            if (!response.ok) {

                throw new Error(
                    "Failed to create product"
                );

            }


            // Get new product
            const newProduct =
                await response.json();


            // Add to local array
            allProducts.push(newProduct);


            // Display cards
            displayProducts(allProducts);


            // Clear form
            productForm.reset();


            // Success message
            formMessage.textContent =
                "Product created successfully!";


            formMessage.className =
                "mt-4 text-green-600 font-semibold";


        } catch (error) {

            console.error(error);


            formMessage.textContent =
                "Failed to create product.";


            formMessage.className =
                "mt-4 text-red-600 font-semibold";


        } finally {

            hideLoading();

        }

    }
);


// =====================================
// BUY NOW
// =====================================

async function buyNow(productId) {

    showLoading();


    try {

        // POST /orders

        const response =
            await fetch(
                `http://127.0.0.1:8000/orders?product_id=${productId}`,
                {
                    method: "POST"
                }
            );


        // Convert response to JSON

        const data =
            await response.json();
        console.log("Order response:", data);


        // =================================
        // SUCCESS
        // =================================

        if (response.ok) {

            // Green banner

            showBanner(
                "Purchase successfull!",
                "success"
            );


            // Find product

            const product =
                allProducts.find(
                    p => p.id === productId
                );


            // Update stock

            if (product) {

                product.stock =
                    data.remaining_stock;

            }


            // Display updated card

            displayProducts(
                allProducts
            );

        }


        // =================================
        // ERROR / OUT OF STOCK
        // =================================

        else {

            // Red banner

            showBanner(
                data.detail,
                "error"
            );

        }


    } catch (error) {

        console.error("Order erroe:",error);


        showBanner(
            "Something went wrong",
            "error"
        );


    } finally {

        hideLoading();

    }

}


// =====================================
// START APPLICATION
// =====================================

loadProducts();