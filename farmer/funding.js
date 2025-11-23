document.addEventListener("DOMContentLoaded", () => {

    // --------------------------- API Helper ---------------------------
    async function apiCall(url, body = null) {
        let options = body ? { method: "POST", body } : { method: "GET" };
        const res = await fetch(url, options);
        return res.json();
    }

    function showToast(message, error = false) {
        const toast = document.getElementById("toast");
        const messageBox = document.getElementById("toast-message");

        messageBox.textContent = message;
        toast.classList.toggle("error", error);
        toast.classList.add("active");

        setTimeout(() => toast.classList.remove("active"), 3000);
    }

    // --------------------------- DOM Elements ---------------------------
    const totalRequestedEl = document.getElementById("total-requested");
    const availableFundsEl = document.getElementById("available-funds");
    const additionalNeededEl = document.getElementById("additional-needed");
    const fundingList = document.getElementById("funding-list");

    const requestModal = document.getElementById("request-modal");
    const createRequestBtn = document.getElementById("create-request-btn");
    const submitRequestBtn = document.getElementById("submit-request");
    const cancelRequestBtn = document.getElementById("cancel-request");

    const purposeBoxes = document.querySelectorAll(".purpose");
    const otherPurposeCheck = document.querySelector(".purpose-other");
    const otherPurposeBox = document.getElementById("other-purpose-box");
    const customPurposeInput = document.getElementById("custom-purpose");

    const requestAmountEl = document.getElementById("request-amount");
    const requestDescriptionEl = document.getElementById("request-description");

    let hasPending = false; // Track pending status


    // --------------------------- Purpose Logic ---------------------------
    purposeBoxes.forEach(box => {
        box.addEventListener("change", () => {
            const checked = [...purposeBoxes].filter(p => p.checked);

            if (checked.length > 3) {
                box.checked = false;
                showToast("You can select a maximum of 3 purposes.", true);
                return;
            }

            otherPurposeBox.style.display = otherPurposeCheck.checked ? "block" : "none";

            if (!otherPurposeCheck.checked) customPurposeInput.value = "";
        });
    });


    // --------------------------- Modal Logic ---------------------------
    createRequestBtn.addEventListener("click", () => {
        if (hasPending) {
            showToast("You already have a pending request. Please wait for approval.", true);
            return;
        }

        resetForm();
        requestModal.classList.add("active");
    });

    cancelRequestBtn.addEventListener("click", () => {
        requestModal.classList.remove("active");
    });

    window.addEventListener("click", e => {
        if (e.target === requestModal) requestModal.classList.remove("active");
    });


    // --------------------------- VALIDATION FUNCTION ---------------------------
    function validateRequest(amount, description, selected) {

        if (!amount || Number(amount) <= 0) {
            showToast("Enter a valid amount greater than 0.", true);
            requestAmountEl.style.border = "2px solid red";
            return false;
        }
        requestAmountEl.style.border = "";

        if (!description || description.trim().length < 10) {
            showToast("Description must be at least 10 characters.", true);
            requestDescriptionEl.style.border = "2px solid red";
            return false;
        }
        requestDescriptionEl.style.border = "";

        if (selected.length === 0) {
            showToast("Select at least one purpose.", true);
            return false;
        }

        if (selected.length > 3) {
            showToast("You can select a maximum of 3 purposes.", true);
            return false;
        }

        if (selected.includes("other")) {
            const txt = customPurposeInput.value.trim();
            if (!txt) {
                showToast("Enter custom purpose.", true);
                customPurposeInput.style.border = "2px solid red";
                return false;
            }
            customPurposeInput.style.border = "";
        }

        return true;
    }


    // --------------------------- Submit Request ---------------------------
    let submitting = false;

    submitRequestBtn.addEventListener("click", async () => {
        if (submitting) return;
        submitting = true;
        submitRequestBtn.disabled = true;

        const amount = requestAmountEl.value;
        const description = requestDescriptionEl.value;

        const selected = [...purposeBoxes].filter(p => p.checked).map(p => p.value);

        // --- VALIDATIONS ---
        if (!validateRequest(amount, description, selected)) {
            submitting = false;
            submitRequestBtn.disabled = false;
            return;
        }

        let finalPurpose = "";
        if (selected.includes("other")) {
            const txt = customPurposeInput.value.trim();
            finalPurpose = selected.map(p => p === "other" ? `other:${txt}` : p).join(",");
        } else {
            finalPurpose = selected.join(",");
        }

        const fd = new FormData();
        fd.append("amount", amount);
        fd.append("purpose", finalPurpose);
        fd.append("description", description);

        const out = await apiCall("../backend/funding/create_request.php", fd);

        submitting = false;
        submitRequestBtn.disabled = false;

        if (out.status !== "OK") {
            showToast(out.message, true);
            return;
        }

        showToast("Funding request submitted!");

        requestModal.classList.remove("active");

        loadSummary();
        loadRequests();
    });


    // --------------------------- Load Summary ---------------------------
    async function loadSummary() {
        const out = await apiCall("../backend/funding/summary.php");
        if (out.status !== "OK") return;

        totalRequestedEl.textContent = out.data.total_requested;
        availableFundsEl.textContent = out.data.available_funds;
        additionalNeededEl.textContent = out.data.additional_needed;
    }


    // --------------------------- Load Request List ---------------------------
    async function loadRequests() {
        const out = await apiCall("../backend/funding/list_requests.php");
        fundingList.innerHTML = "";

        hasPending = false;

        if (out.status !== "OK" || out.data.length === 0) {
            fundingList.innerHTML = `<div style="color:#777;">No funding requests yet.</div>`;
            return;
        }

        out.data.forEach(req => {

            if (req.status === "pending") {
                hasPending = true; // block new requests
            }

            const row = document.createElement("div");
            row.style.cssText = `
                padding: 12px;
                border-bottom: 1px solid #eee;
                display:flex;
                justify-content: space-between;
            `;

            row.innerHTML = `
                <div>
                    <div style="font-weight:bold;">${req.amount_tokens} Tokens</div>
                    <div style="color:#666;font-size:.9rem;">
                        ${req.purpose} • ${req.description}
                    </div>
                </div>
                <div style="font-weight:bold;
                    color:${
                        req.status === "approved" ? "#4caf50" :
                        req.status === "rejected" ? "#f44336" : "#ff9800"
                    };">
                    ${req.status}
                </div>
            `;

            fundingList.appendChild(row);
        });
    }


    // --------------------------- RESET FORM ---------------------------
    function resetForm() {
        requestAmountEl.value = "";
        requestDescriptionEl.value = "";
        customPurposeInput.value = "";
        requestAmountEl.style.border = "";
        requestDescriptionEl.style.border = "";

        purposeBoxes.forEach(p => p.checked = false);
        otherPurposeBox.style.display = "none";
    }


    // --------------------------- INIT ---------------------------
    loadSummary();
    loadRequests();

});
