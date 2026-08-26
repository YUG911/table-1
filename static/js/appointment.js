document.addEventListener("DOMContentLoaded", function () {

    /* =========================================
       GET ALL ELEMENTS
    ========================================= */

    const doctorImage =
        document.getElementById("doctorImage");

    const doctorName =
        document.getElementById("doctorName");

    const doctorSpecialization =
        document.getElementById("doctorSpecialization");

    const doctorClinic =
        document.getElementById("doctorClinic");

    const doctorLocation =
        document.getElementById("doctorLocation");

    const doctorRating =
        document.getElementById("doctorRating");

    const summaryDoctorImage =
        document.getElementById("summaryDoctorImage");

    const summaryDoctorName =
        document.getElementById("summaryDoctorName");

    const summarySpecialization =
        document.getElementById("summarySpecialization");

    const summaryLocation =
        document.getElementById("summaryLocation");

    const consultationFee =
        document.getElementById("consultationFee");

    const summaryDate =
        document.getElementById("summaryDate");

    const summaryTime =
        document.getElementById("summaryTime");


    /* =========================================
       DEFAULT DOCTOR
    ========================================= */

    const defaultDoctor = {

        name: "Dr. Rahul Sharma",

        specialization: "Cardiologist",

        clinic: "Well-Point Heart Clinic",

        location: "Mehsana, Gujarat",

        rating: "4.8",

        fee: "₹500",

        image:
            "https://randomuser.me/api/portraits/men/32.jpg"

    };


    /* =========================================
       LOAD SELECTED DOCTOR
    ========================================= */

    let selectedDoctor = defaultDoctor;


    const savedDoctor =
        localStorage.getItem("selectedDoctor");


    if (savedDoctor) {

        try {

            selectedDoctor =
                JSON.parse(savedDoctor);

        }

        catch (error) {

            console.log(
                "Could not load selected doctor"
            );

        }

    }


    /* =========================================
       DISPLAY SELECTED DOCTOR
    ========================================= */

    function displayDoctor() {

        doctorImage.src =
            selectedDoctor.image || defaultDoctor.image;


        summaryDoctorImage.src =
            selectedDoctor.image || defaultDoctor.image;


        doctorName.textContent =
            selectedDoctor.name || defaultDoctor.name;


        summaryDoctorName.textContent =
            selectedDoctor.name || defaultDoctor.name;


        doctorSpecialization.textContent =
            selectedDoctor.specialization ||
            defaultDoctor.specialization;


        summarySpecialization.textContent =
            selectedDoctor.specialization ||
            defaultDoctor.specialization;


        doctorClinic.textContent =
            selectedDoctor.clinic ||
            defaultDoctor.clinic;


        doctorLocation.textContent =
            selectedDoctor.location ||
            defaultDoctor.location;


        summaryLocation.textContent =
            selectedDoctor.location ||
            defaultDoctor.location;


        doctorRating.textContent =
            selectedDoctor.rating ||
            defaultDoctor.rating;


        consultationFee.textContent =
            selectedDoctor.fee ||
            defaultDoctor.fee;

    }


    displayDoctor();


    /* =========================================
       DATE SELECTION
    ========================================= */

    const dateButtons =
        document.querySelectorAll(".date-btn");


    let selectedDate =
        document.querySelector(".date-btn.active")
        .dataset.date;


    dateButtons.forEach(function (button) {

        button.addEventListener(
            "click",
            function () {

                dateButtons.forEach(function (btn) {

                    btn.classList.remove("active");

                });


                button.classList.add("active");


                selectedDate =
                    button.dataset.date;


                updateSummary();

            }
        );

    });


    /* =========================================
       TIME SELECTION
    ========================================= */

    const timeButtons =
        document.querySelectorAll(".time-btn");


    let selectedTime =
        document.querySelector(".time-btn.active")
        .textContent.trim();


    timeButtons.forEach(function (button) {

        button.addEventListener(
            "click",
            function () {

                timeButtons.forEach(function (btn) {

                    btn.classList.remove("active");

                });


                button.classList.add("active");


                selectedTime =
                    button.textContent.trim();


                updateSummary();

            }
        );

    });


    /* =========================================
       UPDATE SUMMARY
    ========================================= */

    function updateSummary() {

        summaryDate.textContent =
            selectedDate;


        summaryTime.textContent =
            selectedTime;

    }


    updateSummary();


    /* =========================================
       CONFIRM APPOINTMENT
    ========================================= */

    const confirmButton =
        document.getElementById("confirmAppointment");


    const patientName =
        document.getElementById("patientName");


    const patientPhone =
        document.getElementById("patientPhone");


    const patientEmail =
        document.getElementById("patientEmail");


    const reason =
        document.getElementById("reason");


    const successModal =
        document.getElementById("successModal");


    const successMessage =
        document.getElementById("successMessage");


    const closeModal =
        document.getElementById("closeModal");


    confirmButton.addEventListener(
        "click",
        function () {

            const name =
                patientName.value.trim();


            const phone =
                patientPhone.value.trim();


            const email =
                patientEmail.value.trim();


            const appointmentReason =
                reason.value.trim();


            /* Check required fields */

            if (
                name === "" ||
                phone === "" ||
                email === "" ||
                appointmentReason === ""
            ) {

                alert(
                    "Please fill in all your appointment details."
                );

                return;

            }


            /* Appointment object */

            const appointment = {

                doctor:
                    selectedDoctor,

                patientName:
                    name,

                patientPhone:
                    phone,

                patientEmail:
                    email,

                reason:
                    appointmentReason,

                date:
                    selectedDate,

                time:
                    selectedTime

            };


            /* Save temporary appointment */

            localStorage.setItem(
                "appointmentDetails",
                JSON.stringify(appointment)
            );


            /* Update success message */

            successMessage.textContent =
                `Your appointment request with ${selectedDoctor.name || defaultDoctor.name} has been submitted for ${selectedDate} at ${selectedTime}.`;


            /* Show modal */

            successModal.classList.add("show");

        }
    );


    /* =========================================
       CLOSE MODAL
    ========================================= */

    closeModal.addEventListener(
    "click",
    function () {

        successModal.classList.remove("show");

        window.location.href = "/doctors/";
    }
);


    /* Close when clicking outside */

    successModal.addEventListener(
        "click",
        function (event) {

            if (event.target === successModal) {

                successModal.classList.remove("show");

            }

        }
    );

});