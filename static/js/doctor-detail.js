// =========================
// GET ELEMENTS
// =========================

const dateOptions =
    document.querySelectorAll(".date-option");

const timeSlots =
    document.querySelectorAll(".time-slot");

const selectedAppointmentText =
    document.getElementById(
        "selectedAppointmentText"
    );

const bookAppointmentBtn =
    document.getElementById(
        "bookAppointmentBtn"
    );

const mobileMenuBtn =
    document.getElementById(
        "mobileMenuBtn"
    );

const mobileMenu =
    document.getElementById(
        "mobileMenu"
    );


// =========================
// SELECTED VALUES
// =========================

let selectedDate = "Today";

let selectedTime = "";


// =========================
// DATE SELECTION
// =========================

dateOptions.forEach(
    function (date) {

        date.addEventListener(
            "click",
            function () {

                // Remove active class

                dateOptions.forEach(
                    function (item) {

                        item.classList.remove(
                            "active"
                        );

                    }
                );


                // Add active class

                date.classList.add(
                    "active"
                );


                // Get date information

                const day =
                    date.querySelector("span")
                        .textContent;

                const number =
                    date.querySelector("strong")
                        .textContent;

                const month =
                    date.querySelector("small")
                        .textContent;


                selectedDate =
                    day +
                    ", " +
                    number +
                    " " +
                    month;


                updateSelectedAppointment();

            }
        );

    }
);


// =========================
// TIME SELECTION
// =========================

timeSlots.forEach(
    function (slot) {

        slot.addEventListener(
            "click",
            function () {

                // Remove active class

                timeSlots.forEach(
                    function (item) {

                        item.classList.remove(
                            "active"
                        );

                    }
                );


                // Add active class

                slot.classList.add(
                    "active"
                );


                // Save selected time

                selectedTime =
                    slot.textContent.trim();


                updateSelectedAppointment();

            }
        );

    }
);


// =========================
// UPDATE APPOINTMENT TEXT
// =========================

function updateSelectedAppointment() {

    if (selectedTime === "") {

        selectedAppointmentText.textContent =
            selectedDate +
            " • Select a time";

    }

    else {

        selectedAppointmentText.textContent =
            selectedDate +
            " • " +
            selectedTime;

    }

}


// =========================
// BOOK APPOINTMENT VALIDATION
// =========================

bookAppointmentBtn.addEventListener(
    "click",
    function (event) {

        if (selectedTime === "") {

            event.preventDefault();

            alert(
                "Please select an appointment time."
            );

        }

        else {

            // Save selected appointment temporarily

            sessionStorage.setItem(
                "selectedDate",
                selectedDate
            );


            sessionStorage.setItem(
                "selectedTime",
                selectedTime
            );

        }

    }
);


// =========================
// MOBILE MENU
// =========================

mobileMenuBtn.addEventListener(
    "click",
    function () {

        mobileMenu.classList.toggle(
            "show"
        );

    }
);


// =========================
// INITIAL DISPLAY
// =========================

updateSelectedAppointment();