// search.js
$(document).ready(function() {
    function createPaginationLink(page, isActive, text) {
        return `<a href="#" class="${isActive ? 'active' : ''}" data-page="${page}">${text || page}</a>`;
    }

    function bindPaginationClickEvents() {
        $(".pagination a").on("click", function(event) {
            event.preventDefault();
            const page = $(this).data("page");
            loadProducts($('#search-input').val(), page);
        });
    }


    function createPaginationLinks(pagination) {
        let html = '';
        const totalPages = pagination.total_pages;
        const currentPage = pagination.current_page;
        const windowSize = 3; // Number of pages to show around the current page

        if (pagination.has_prev) {
            html += createPaginationLink(1, false, 'First');
            html += createPaginationLink(pagination.prev_num, false, 'Previous');
        }

        // First Pages
        for (let p = 1; p <= 4; p++) {
            if (p < currentPage - windowSize) {
                html += createPaginationLink(p, false);
            }
        }

        // Ellipses after the first pages
        if (currentPage - windowSize > 4) {
            html += '<span>...</span>';
        }

        // Pages around current page
        let startPage = Math.max(currentPage - windowSize, 1);
        let endPage = Math.min(currentPage + windowSize, totalPages);

        for (let p = startPage; p <= endPage; p++) {
            html += createPaginationLink(p, p === currentPage);
        }

        // Ellipses before the last pages
        if (currentPage + windowSize < totalPages - 3) {
            html += '<span>...</span>';
        }

        // Last Pages
        for (let p = totalPages - 1; p <= totalPages; p++) {
            if (p > currentPage + windowSize) {
                html += createPaginationLink(p, false);
            }
        }

        if (pagination.has_next) {
            html += createPaginationLink(pagination.next_num, false, 'Next');
            html += createPaginationLink(totalPages, false, 'Last');
        }

        return html;
    }

    function attachFilterEventListeners() {
        $('#category, #condition, #dateposted, #status, #price').on('change', function() {
            loadProducts($('#search-input').val());
        });
    }



    // Function to load products based on the query and page number
    function loadProducts(query, page = 1) {
        // Gather filter parameters
        var category = $('#category').val();
        var condition = $('#condition').val();
        var datePosted = $('#dateposted').val();
        var status = $('#status').val();
        var price = $('#price').val();

        // console.log("Date Posted:", datePosted);


        $.ajax({
            url: "/ajax_search",
            data: {
                search_query: query,
                page: page,
                category: category,
                condition: condition,
                date_posted: datePosted,
                status: status,
                price: price
                },
            type: 'GET',
            success: function(response) {
                $(".products-container").empty();
                $(".pagination").empty();

                if (response.products.length === 0) {
                    $(".products-container").append('<p>No products found.</p>');
                } else {
                    response.products.forEach(function(product) {
                        $(".products-container").append(`
                            <div class="product-card">
                                <img src="${product.image_url}" alt="Product Image">
                                <div class="product-info">
                                    <h5>${product.name}</h5>
                                    <p class="color">Color: ${product.color}</p>
                                    <p class="condition">Condition: ${product.condition}</p>
                                    <p class="date-posted">Posted on: ${product.date_posted}</p>
                                    <p class="price">$${product.price}</p>
                                </div>
                            </div>
                        `);
                    });

                        // Update pagination
                        $(".pagination").html(createPaginationLinks(response.pagination));

                        // Bind click events to pagination links
                        bindPaginationClickEvents();
                }
            }
        });
    }
    // Attach event listeners to filter elements
    attachFilterEventListeners();

    // Update products based on search input
    $("#search-input").on("input", function() {
        var query = $(this).val();
        loadProducts(query);
    });

    // Initial load
    loadProducts('');
});
