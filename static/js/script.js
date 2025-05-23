document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');

    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent default form submission

        let isValid = true; // Flag to track overall form validity
        const formData = {}; // Use a plain object to build JSON data

        // --- Personal Information Validation and Data Collection ---
        const fullNameInput = document.getElementById('fullName');
        if (fullNameInput.value.trim() === '') {
            alert('Please enter your full name.');
            fullNameInput.focus();
            isValid = false;
        } else {
            formData.full_name = fullNameInput.value.trim(); // Match serializer field name
        }

        const phoneNumberInput = document.getElementById('phoneNumber');
        const phoneNumberPattern = /^\d{10}$/;
        if (!phoneNumberPattern.test(phoneNumberInput.value.trim())) {
            alert('Please enter a valid 10-digit phone number.');
            phoneNumberInput.focus();
            isValid = false;
        } else {
            formData.phone_number = phoneNumberInput.value.trim(); // Match serializer field name
        }

        const emailAddressInput = document.getElementById('emailAddress');
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(emailAddressInput.value.trim())) {
            alert('Please enter a valid email address.');
            emailAddressInput.focus();
            isValid = false;
        } else {
            formData.email_address = emailAddressInput.value.trim(); // Match serializer field name
        }

        const addressInput = document.getElementById('address');
        formData.address = addressInput.value.trim(); // Address is optional

        // --- Vehicle Information Validation and Data Collection ---
        const tataModelSelect = document.getElementById('tataModel');
        if (tataModelSelect.value === '') {
            alert('Please select your vehicle model.');
            tataModelSelect.focus();
            isValid = false;
        } else {
            formData.tata_model = tataModelSelect.value; // Match serializer field name
        }

        const regYearInput = document.getElementById('regYear');
        const currentYear = new Date().getFullYear();
        const enteredYear = parseInt(regYearInput.value, 10);
        if (isNaN(enteredYear) || enteredYear < 1900 || enteredYear > currentYear) {
            alert(`Please enter a valid registration year (between 1900 and ${currentYear}).`);
            regYearInput.focus();
            isValid = false;
        } else {
            formData.reg_year = enteredYear; // Match serializer field name
        }

        const regNumberInput = document.getElementById('regNumber');
        if (regNumberInput.value.trim() === '') {
            alert('Please enter your vehicle registration number.');
            regNumberInput.focus();
            isValid = false;
        } else {
            formData.reg_number = regNumberInput.value.trim(); // Match serializer field name
        }

        const odometerReadingInput = document.getElementById('odometerReading');
        const odometerReading = parseInt(odometerReadingInput.value, 10);
        if (isNaN(odometerReading) || odometerReading < 0) {
            alert('Please enter a valid odometer reading (a non-negative number).');
            odometerReadingInput.focus();
            isValid = false;
        } else {
            formData.odometer_reading = odometerReading; // Match serializer field name
        }

        // --- Service Details Validation and Data Collection ---
        const serviceTypeRadios = document.querySelectorAll('input[name="serviceType"]');
        let serviceTypeSelected = false;
        for (const radio of serviceTypeRadios) {
            if (radio.checked) {
                formData.service_type = radio.value; // Match serializer field name
                serviceTypeSelected = true;
                break;
            }
        }
        if (!serviceTypeSelected) {
            alert('Please select a service type.');
            isValid = false;
        }

        const commonIssuesCheckboxes = document.querySelectorAll('input[name="commonIssues"]:checked');
        formData.common_issues = Array.from(commonIssuesCheckboxes).map(cb => cb.value); // Collect checked values as an array

        const otherIssueCheckbox = document.getElementById('otherIssue');
        const additionalDetailsTextarea = document.getElementById('additionalDetails');
        if (otherIssueCheckbox.checked && additionalDetailsTextarea.value.trim() === '') {
            alert('Please provide details for "Other Issue".');
            additionalDetailsTextarea.focus();
            isValid = false;
        } else {
            formData.additional_details = additionalDetailsTextarea.value.trim();
        }

        // --- Appointment Details Validation and Data Collection ---
        const preferredDateInput = document.getElementById('preferredDate');
        const selectedDate = new Date(preferredDateInput.value);
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        if (preferredDateInput.value.trim() === '') {
            alert('Please select a preferred date for the appointment.');
            preferredDateInput.focus();
            isValid = false;
        } else if (selectedDate < today) {
            alert('The preferred date cannot be in the past. Please select a future date.');
            preferredDateInput.focus();
            isValid = false;
        } else {
            formData.preferred_date = preferredDateInput.value; // Send as 'YYYY-MM-DD' string
        }

        const preferredTimeSlotSelect = document.getElementById('preferredTimeSlot');
        if (preferredTimeSlotSelect.value === '') {
            alert('Please select a preferred time slot.');
            preferredTimeSlotSelect.focus();
            isValid = false;
        } else {
            formData.preferred_time_slot = preferredTimeSlotSelect.value; // Match serializer field name
        }

        // --- Additional Preferences Data Collection ---
        const servicePrefCheckboxes = document.querySelectorAll('input[name="servicePref"]:checked');
        formData.service_pref = Array.from(servicePrefCheckboxes).map(cb => cb.value); // Collect checked values as an array

        // If any validation failed, stop here
        if (!isValid) {
            console.log('Form validation failed.');
            return;
        }

        // --- Submission to Localhost DRF Endpoint ---
        console.log('Client-side validation passed. Attempting to submit to DRF API...');
        console.log('Data to be sent:', formData); // For debugging

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const apiEndpoint = 'http://127.0.0.1:8000/api/service-requests/'; // Your DRF API endpoint for list/create

        try {
            const response = await fetch(apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', // Important for sending JSON
                    'X-CSRFToken': csrfToken, // Important for Django's CSRF protection
                },
                body: JSON.stringify(formData), // Convert the formData object to a JSON string
            });

            if (response.ok) {
                const result = await response.json();
                console.log('API response (Success):', result);
                window.location.href = `/confirmation?id=${result.id}`;
            } else {
                const errorData = await response.json(); // DRF often sends validation errors as JSON
                console.error('API error:', response.status, errorData);

                let errorMessage = 'Failed to submit service request. Please check your inputs.';
                if (errorData && typeof errorData === 'object') {
                    // Attempt to parse DRF validation errors
                    const detailErrors = Object.keys(errorData).map(key => {
                        const errorValue = errorData[key];
                        if (Array.isArray(errorValue)) {
                            return `${key}: ${errorValue.join(', ')}`;
                        }
                        return `${key}: ${errorValue}`;
                    }).join('\n');
                    if (detailErrors) {
                        errorMessage += '\nDetails:\n' + detailErrors;
                    } else if (errorData.detail) { // For non-field errors or other DRF errors
                         errorMessage += `\n${errorData.detail}`;
                    }
                }
                alert(errorMessage);
            }
        } catch (error) {
            console.error('Network or fetch error:', error);
            alert('An unexpected error occurred while submitting your request. Please try again later.');
        }
    });
});