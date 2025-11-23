const state = {
            tokenBalance: 0,
            transactions: [],
            updates: []
        };

        // DOM Elements
        const pages = document.querySelectorAll('.page');
        const navLinks = document.querySelectorAll('.nav-link');
        const categoryFilters = document.querySelectorAll('.category-filter');
        const productCards = document.querySelectorAll('.product-card');
        const buyButtons = document.querySelectorAll('.buy-button');
        const tokenBalanceElements = document.querySelectorAll('.token-balance, .balance-amount');
        const transactionTable = document.querySelector('.transaction-history tbody');
        const purchaseModal = document.getElementById('purchase-modal');
        const purchaseDetails = document.getElementById('purchase-details');
        const confirmPurchaseBtn = document.getElementById('confirm-purchase');
        const cancelPurchaseBtn = document.getElementById('cancel-purchase');
        const requestModal = document.getElementById('request-modal');
        const requestFundsBtn = document.getElementById('request-funds-btn');
        const createRequestBtn = document.getElementById('create-request-btn');
        const submitRequestBtn = document.getElementById('submit-request');
        const cancelRequestBtn = document.getElementById('cancel-request');
        const submitUpdateBtn = document.getElementById('submit-update');
        const fileUploadContainer = document.getElementById('file-upload-container');
        const fileUploadInput = document.getElementById('update-photo');
        const imagePreview = document.getElementById('image-preview');
        const previewImage = document.getElementById('preview-image');
        const removeImageBtn = document.getElementById('remove-image');
        const updatesList = document.getElementById('updates-list');
        const toast = document.getElementById('toast');
        const toastMessage = document.getElementById('toast-message');

        // Current purchase item
        let currentPurchase = null;

        // Initialize the application
        function init() {
            // Set up navigation
            navLinks.forEach(link => {
                link.addEventListener('click', handleNavigation);
            });

            // Set up marketplace filters
            categoryFilters.forEach(filter => {
                filter.addEventListener('click', handleCategoryFilter);
            });

            // Set up purchase buttons
            buyButtons.forEach(button => {
                button.addEventListener('click', handlePurchaseClick);
            });

            // Set up modal buttons
            confirmPurchaseBtn.addEventListener('click', handleConfirmPurchase);
            cancelPurchaseBtn.addEventListener('click', () => purchaseModal.classList.remove('active'));
            document.querySelectorAll('.close-modal').forEach(btn => {
                btn.addEventListener('click', () => {
                    purchaseModal.classList.remove('active');
                    requestModal.classList.remove('active');
                });
            });

            // Set up funding request buttons
            requestFundsBtn.addEventListener('click', () => requestModal.classList.add('active'));
            createRequestBtn.addEventListener('click', () => requestModal.classList.add('active'));
            submitRequestBtn.addEventListener('click', handleSubmitRequest);
            cancelRequestBtn.addEventListener('click', () => requestModal.classList.remove('active'));

            // Set up enhanced update functionality
            fileUploadContainer.addEventListener('click', () => fileUploadInput.click());
            fileUploadContainer.addEventListener('dragover', handleDragOver);
            fileUploadContainer.addEventListener('dragleave', handleDragLeave);
            fileUploadContainer.addEventListener('drop', handleDrop);
            fileUploadInput.addEventListener('change', handleFileSelect);
            removeImageBtn.addEventListener('click', removeImage);
            submitUpdateBtn.addEventListener('click', handleSubmitUpdate);

            // Close modals when clicking outside
            window.addEventListener('click', (e) => {
                if (e.target === purchaseModal) purchaseModal.classList.remove('active');
                if (e.target === requestModal) requestModal.classList.remove('active');
            });

            // Render initial data
            renderTransactions();
            renderUpdates();
            updateTokenBalance();

            // Set today's date as default
            document.getElementById('update-date').valueAsDate = new Date();
        }

        // Navigation handler
        function handleNavigation(e) {
            if (this.id === "logout-btn" || this.id === "estimator-btn") return;

            e.preventDefault();

            navLinks.forEach(link => link.classList.remove('active'));
            pages.forEach(page => page.classList.remove('active'));

            this.classList.add('active');
            const pageId = this.getAttribute('data-page');
            document.getElementById(pageId).classList.add('active');
        }



        // Category filter handler
        function handleCategoryFilter() {
            // Remove active class from all filters
            categoryFilters.forEach(filter => filter.classList.remove('active'));

            // Add active class to clicked filter
            this.classList.add('active');

            const category = this.getAttribute('data-category');

            // Show/hide products based on category
            productCards.forEach(product => {
                if (category === 'all' || product.getAttribute('data-category') === category) {
                    product.style.display = 'block';
                } else {
                    product.style.display = 'none';
                }
            });
        }

        // Purchase click handler
        function handlePurchaseClick() {
            const itemName = this.getAttribute('data-item');
            const itemPrice = parseInt(this.getAttribute('data-price'));

            currentPurchase = { name: itemName, price: itemPrice };

            // Update purchase modal content
            purchaseDetails.innerHTML = `
                <p>You are about to purchase:</p>
                <p style="font-weight: bold; margin: 10px 0;">${itemName}</p>
                <p>Price: <span style="color: var(--primary); font-weight: bold;">${itemPrice} Tokens</span></p>
                <p>Your current balance: <span style="font-weight: bold;">${state.tokenBalance} Tokens</span></p>
                <p>Balance after purchase: <span style="font-weight: bold;">${state.tokenBalance - itemPrice} Tokens</span></p>
            `;

            // Enable/disable confirm button based on balance
            if (state.tokenBalance >= itemPrice) {
                confirmPurchaseBtn.disabled = false;
                confirmPurchaseBtn.style.backgroundColor = '';
            } else {
                confirmPurchaseBtn.disabled = true;
                confirmPurchaseBtn.style.backgroundColor = '#9e9e9e';
            }

            // Show modal
            purchaseModal.classList.add('active');
        }

        // Confirm purchase handler
        function handleConfirmPurchase() {
            if (!currentPurchase) return;

            const { name, price } = currentPurchase;

            if (state.tokenBalance >= price) {
                // Update token balance
                state.tokenBalance -= price;

                // Add transaction
                const today = new Date().toISOString().split('T')[0];
                state.transactions.unshift({
                    date: today,
                    description: `${name} purchase`,
                    amount: -price,
                    balance: state.tokenBalance
                });

                // Update UI
                updateTokenBalance();
                renderTransactions();

                // Show success message
                showToast(`Successfully purchased ${name} for ${price} tokens!`);

                // Close modal
                purchaseModal.classList.remove('active');
                currentPurchase = null;
            } else {
                showToast('Insufficient tokens to complete this purchase.', true);
            }
        }

        // Submit funding request handler
        function handleSubmitRequest() {
            const amount = document.getElementById('request-amount').value;
            const purpose = document.getElementById('request-purpose').value;
            const description = document.getElementById('request-description').value;

            if (!amount || !description) {
                showToast('Please fill in all fields.', true);
                return;
            }

            // In a real app, this would send a request to the server
            showToast(`Funding request for ${amount} tokens submitted successfully!`);

            // Reset form and close modal
            document.getElementById('request-amount').value = '';
            document.getElementById('request-description').value = '';
            requestModal.classList.remove('active');
        }

        // Drag and drop handlers for image upload
        function handleDragOver(e) {
            e.preventDefault();
            fileUploadContainer.classList.add('dragover');
        }

        function handleDragLeave(e) {
            e.preventDefault();
            fileUploadContainer.classList.remove('dragover');
        }

        function handleDrop(e) {
            e.preventDefault();
            fileUploadContainer.classList.remove('dragover');

            if (e.dataTransfer.files.length) {
                fileUploadInput.files = e.dataTransfer.files;
                handleFileSelect();
            }
        }

        // File selection handler
        function handleFileSelect() {
            const file = fileUploadInput.files[0];

            if (file) {
                if (file.type.startsWith('image/')) {
                    const reader = new FileReader();

                    reader.onload = function (e) {
                        previewImage.src = e.target.result;
                        imagePreview.style.display = 'block';
                    };

                    reader.readAsDataURL(file);
                } else {
                    showToast('Please select a valid image file.', true);
                }
            }
        }

        // Remove image handler
        function removeImage() {
            fileUploadInput.value = '';
            imagePreview.style.display = 'none';
        }

        // Submit update handler
        function handleSubmitUpdate() {
            const date = document.getElementById('update-date').value;
            const day = document.getElementById('update-day').value;
            const title = document.getElementById('update-title').value;
            const description = document.getElementById('update-description').value;
            const imageFile = fileUploadInput.files[0];

            if (!date || !day || !title || !description) {
                showToast('Please fill in all fields.', true);
                return;
            }

            // Create new update object
            const newUpdate = {
                id: state.updates.length + 1,
                date: date,
                day: parseInt(day),
                title: title,
                description: description
            };

            // Handle image if provided
            if (imageFile) {
                const reader = new FileReader();

                reader.onload = function (e) {
                    newUpdate.image = e.target.result;
                    addUpdateToState(newUpdate);
                };

                reader.readAsDataURL(imageFile);
            } else {
                addUpdateToState(newUpdate);
            }
        }

        // Add update to state and re-render
        function addUpdateToState(update) {
            // Add to beginning of updates array
            state.updates.unshift(update);

            // Re-render updates
            renderUpdates();

            // Reset form
            document.getElementById('update-title').value = '';
            document.getElementById('update-description').value = '';
            removeImage();

            // Show success message
            showToast('Farm update published successfully!');
        }

        // Render updates list
        function renderUpdates() {
            // Clear existing updates
            updatesList.innerHTML = '';

            if (state.updates.length === 0) {
                // Show empty state
                updatesList.innerHTML = `
                    <div class="empty-state">
                        <i class="fas fa-images"></i>
                        <h3>No updates yet</h3>
                        <p>Share your first farm update to keep investors informed.</p>
                    </div>
                `;
                return;
            }

            // Add each update to the list
            state.updates.forEach(update => {
                const updateElement = document.createElement('div');
                updateElement.className = 'update-card';

                updateElement.innerHTML = `
                    <div class="update-header">
                        <div class="update-date">
                            <i class="far fa-calendar"></i>
                            ${formatDate(update.date)}
                        </div>
                        <div class="update-day">Day ${update.day}</div>
                    </div>
                    <div class="update-content">
                        <div class="update-title">${update.title}</div>
                        <div class="update-description">${update.description}</div>
                        ${update.image ? `<img src="${update.image}" alt="Farm update" class="update-image">` : ''}
                    </div>
                `;

                updatesList.appendChild(updateElement);
            });
        }

        // Update token balance in UI
        function updateTokenBalance() {
            tokenBalanceElements.forEach(element => {
                if (element.classList.contains('balance-amount') && element.parentElement.classList.contains('balance-card')) {
                    // For balance cards, just show the number
                    element.textContent = state.tokenBalance.toLocaleString();
                } else {
                    // For other elements, show with "Tokens"
                    element.textContent = `${state.tokenBalance.toLocaleString()} Tokens`;
                }
            });
        }

        // Render transaction history
        function renderTransactions() {
            // Clear existing rows
            transactionTable.innerHTML = '';

            // Add transactions
            state.transactions.forEach(transaction => {
                const row = document.createElement('tr');

                row.innerHTML = `
                    <td>${transaction.date}</td>
                    <td>${transaction.description}</td>
                    <td class="${transaction.amount > 0 ? 'transaction-positive' : 'transaction-negative'}">
                        ${transaction.amount > 0 ? '+' : ''} ${transaction.amount} Tokens
                    </td>
                    <td>${transaction.balance.toLocaleString()}</td>
                `;

                transactionTable.appendChild(row);
            });
        }

        // Show toast notification
        function showToast(message, isError = false) {
            toastMessage.textContent = message;

            if (isError) {
                toast.classList.add('error');
            } else {
                toast.classList.remove('error');
            }

            toast.classList.add('active');

            setTimeout(() => {
                toast.classList.remove('active');
            }, 3000);
        }

        // Format date for display
        function formatDate(dateString) {
            const options = { year: 'numeric', month: 'long', day: 'numeric' };
            return new Date(dateString).toLocaleDateString(undefined, options);
        }

        // Initialize the app when DOM is loaded
        document.addEventListener('DOMContentLoaded', init);
 async function loadFarmerData() {
            try {
                const response = await fetch("../backend/get-farmer-data.php");
                const result = await response.json();

                if (!result || result.status !== "OK" || !result.data) {
                    console.log("Returned:", result);
                    return alert("Session expired. Please login again.");
                }

                const farmer = result.data;

                // Safe DOM setters
                const setText = (id, value) => {
                    const el = document.getElementById(id);
                    if (el) el.textContent = value ? value : "N/A";
                };

                // Header avatar
                const avatar = document.querySelector(".user-avatar");
                if (avatar) avatar.textContent = farmer.name?.charAt(0) || "F";

                // Header name
                const headerName = document.querySelector(".user-info div div:first-child");
                if (headerName) headerName.textContent = farmer.name || "";

                // Header location
                const headerLoc = document.querySelector(".user-info div div:nth-child(2)");
                if (headerLoc) headerLoc.textContent = farmer.state || "";

                // Dashboard card
                setText("farmer_name", farmer.name);
                setText("farmer_location", farmer.state + ", " + farmer.district);
                setText("farmer_crop", farmer.farming_type);
                setText("farmer_land", farmer.land_area_acres + " Acres");

            } catch (error) {
                console.log("JS ERROR:", error);
                alert("Unable to load farmer details.");
            }
        }

        document.addEventListener("DOMContentLoaded", loadFarmerData);
         async function loadFarmImages() {
            try {
                const res = await fetch("../backend/farmer/get_farm_images.php", {
                    credentials: "include"
                });

                const out = await res.json();
                const grid = document.getElementById("farm-photo-grid");
                const empty = document.getElementById("farm-photo-empty");

                if (!grid || !empty) return;

                // Clear previous grid items
                grid.innerHTML = "";

                if (out.status === "OK" && out.data && Array.isArray(out.data.images) && out.data.images.length > 0) {
                    empty.style.display = "none";

                    out.data.images.forEach(img => {
                        const card = document.createElement("div");
                        card.style.width = "100%";
                        card.style.borderRadius = "10px";
                        card.style.overflow = "hidden";
                        card.style.boxShadow = "0 2px 8px rgba(0,0,0,0.15)";
                        card.style.cursor = "pointer";
                        card.style.background = "#fff";

                        card.innerHTML = `
                    <img src="${img}"
                         style="width:100%; height:110px; object-fit:cover; border-bottom:1px solid #eee;">
                `;

                        grid.appendChild(card);
                    });

                } else {
                    empty.style.display = "block";
                }

            } catch (error) {
                console.error("Farm image load failed:", error);

                document.getElementById("farm-photo-empty").style.display = "block";
            }
        }

        document.addEventListener("DOMContentLoaded", loadFarmImages);
        async function loadSeasonStatus() {
            const phaseEl = document.getElementById("season_phase");
            const dayEl = document.getElementById("season_days");
            const progressEl = document.getElementById("season_progress");
            const startBtn = document.getElementById("startCycleBtn");

            try {
                const res = await fetch("../backend/farmer/get_active_cycle.php", {
                    credentials: "include"
                });

                const out = await res.json();

                if (!out.data) {
                    // No active season
                    phaseEl.textContent = "No active season";
                    dayEl.textContent = "-";
                    progressEl.style.width = "0%";
                    startBtn.style.display = "block";
                    return;
                }

                const c = out.data;
                startBtn.style.display = "none";

                phaseEl.textContent = `${c.phase} (${c.crop_type})`;
dayEl.textContent = `${c.days_passed} of ${c.duration} days`;

                progressEl.style.width = c.progress + "%";

            } catch (err) {
                console.log("Season load error:", err);
            }
        }

        document.addEventListener("DOMContentLoaded", loadSeasonStatus);
        document.getElementById("startCycleBtn").addEventListener("click", function () {
    window.location.href = "start-crop-cycle.html";
});