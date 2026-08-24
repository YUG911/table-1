// =========================
// GET ELEMENTS
// =========================

const searchInput =
    document.getElementById("searchInput");

const locationInput =
    document.getElementById("locationInput");

const searchButton =
    document.getElementById("searchButton");

const doctorCards =
    document.querySelectorAll(".doctor-card");

const specializationFilters =
    document.querySelectorAll(".specialization-filter");

const availabilityFilters =
    document.querySelectorAll(".availability-filter");

const experienceFilters =
    document.querySelectorAll(
        'input[name="experience"]'
    );

const feeFilters =
    document.querySelectorAll(
        'input[name="fee"]'
    );

const doctorCount =
    document.getElementById("doctorCount");

const noResults =
    document.getElementById("noResults");

const clearFilters =
    document.getElementById("clearFilters");

const resetSearch =
    document.getElementById("resetSearch");

const sortDoctors =
    document.getElementById("sortDoctors");

const doctorsList =
    document.getElementById("doctorsList");

const mobileMenuBtn =
    document.getElementById("mobileMenuBtn");

const mobileMenu =
    document.getElementById("mobileMenu");


// =========================
// SEARCH + FILTER FUNCTION
// =========================

function filterDoctors() {

    const searchValue =
        searchInput.value.toLowerCase();

    const locationValue =
        locationInput.value.toLowerCase();


    // Selected specializations

    const selectedSpecializations =
        Array.from(specializationFilters)
            .filter(filter => filter.checked)
            .map(filter => filter.value);


    // Selected availability

    const selectedAvailability =
        Array.from(availabilityFilters)
            .filter(filter => filter.checked)
            .map(filter => filter.value);


    // Selected experience

    const selectedExperience =
        document.querySelector(
            'input[name="experience"]:checked'
        ).value;


    // Selected fee

    const selectedFee =
        document.querySelector(
            'input[name="fee"]:checked'
        ).value;


    let visibleDoctors = 0;


    doctorCards.forEach(function (card) {

        const name =
            card.dataset.name.toLowerCase();

        const specialization =
            card.dataset.specialization;

        const location =
            card.dataset.location.toLowerCase();

        const experience =
            Number(card.dataset.experience);

        const fee =
            Number(card.dataset.fee);

        const availability =
            card.dataset.availability.split(" ");


        // SEARCH MATCH

        const matchesSearch =
            name.includes(searchValue) ||
            specialization
                .toLowerCase()
                .includes(searchValue);


        // LOCATION MATCH

        const matchesLocation =
            location.includes(locationValue);


        // SPECIALIZATION MATCH

        const matchesSpecialization =
            selectedSpecializations.length === 0 ||
            selectedSpecializations.includes(
                specialization
            );


        // EXPERIENCE MATCH

        let matchesExperience = true;


        if (selectedExperience === "1-5") {

            matchesExperience =
                experience >= 1 &&
                experience <= 5;

        }

        else if (selectedExperience === "5-10") {

            matchesExperience =
                experience >= 5 &&
                experience <= 10;

        }

        else if (selectedExperience === "10+") {

            matchesExperience =
                experience >= 10;

        }


        // FEE MATCH

        let matchesFee = true;


        if (selectedFee === "500") {

            matchesFee = fee < 500;

        }

        else if (selectedFee === "1000") {

            matchesFee =
                fee >= 500 &&
                fee <= 1000;

        }

        else if (selectedFee === "above1000") {

            matchesFee =
                fee > 1000;

        }


        // AVAILABILITY MATCH

        const matchesAvailability =
            selectedAvailability.length === 0 ||

            selectedAvailability.some(
                value =>
                    availability.includes(value)
            );


        // FINAL RESULT

        if (
            matchesSearch &&
            matchesLocation &&
            matchesSpecialization &&
            matchesExperience &&
            matchesFee &&
            matchesAvailability
        ) {

            card.style.display = "grid";

            visibleDoctors++;

        }

        else {

            card.style.display = "none";

        }

    });


    // UPDATE COUNT

    doctorCount.textContent =
        visibleDoctors;


    // NO RESULTS

    if (visibleDoctors === 0) {

        noResults.style.display =
            "block";

    }

    else {

        noResults.style.display =
            "none";

    }

}


// =========================
// SEARCH BUTTON
// =========================

searchButton.addEventListener(
    "click",
    filterDoctors
);


// Live search

searchInput.addEventListener(
    "input",
    filterDoctors
);

locationInput.addEventListener(
    "input",
    filterDoctors
);


// =========================
// FILTER EVENTS
// =========================

specializationFilters.forEach(
    function (filter) {

        filter.addEventListener(
            "change",
            filterDoctors
        );

    }
);


availabilityFilters.forEach(
    function (filter) {

        filter.addEventListener(
            "change",
            filterDoctors
        );

    }
);


experienceFilters.forEach(
    function (filter) {

        filter.addEventListener(
            "change",
            filterDoctors
        );

    }
);


feeFilters.forEach(
    function (filter) {

        filter.addEventListener(
            "change",
            filterDoctors
        );

    }
);


// =========================
// CLEAR FILTERS
// =========================

clearFilters.addEventListener(
    "click",
    resetAll
);

resetSearch.addEventListener(
    "click",
    resetAll
);


function resetAll() {

    // Clear search

    searchInput.value = "";

    locationInput.value = "";


    // Clear checkboxes

    specializationFilters.forEach(
        function (filter) {

            filter.checked = false;

        }
    );


    availabilityFilters.forEach(
        function (filter) {

            filter.checked = false;

        }
    );


    // Reset radio buttons

    document.querySelector(
        'input[name="experience"][value="all"]'
    ).checked = true;


    document.querySelector(
        'input[name="fee"][value="all"]'
    ).checked = true;


    filterDoctors();

}


// =========================
// SORT DOCTORS
// =========================

sortDoctors.addEventListener(
    "change",
    function () {

        const cards =
            Array.from(doctorCards);


        cards.sort(function (a, b) {

            if (
                sortDoctors.value ===
                "experience"
            ) {

                return (
                    Number(
                        b.dataset.experience
                    )
                    -
                    Number(
                        a.dataset.experience
                    )
                );

            }


            if (
                sortDoctors.value ===
                "fee-low"
            ) {

                return (
                    Number(a.dataset.fee)
                    -
                    Number(b.dataset.fee)
                );

            }


            if (
                sortDoctors.value ===
                "fee-high"
            ) {

                return (
                    Number(b.dataset.fee)
                    -
                    Number(a.dataset.fee)
                );

            }


            return 0;

        });


        cards.forEach(
            function (card) {

                doctorsList.appendChild(card);

            }
        );

    }
);


// =========================
// MOBILE MENU
// =========================

mobileMenuBtn.addEventListener(
    "click",
    function () {

        mobileMenu.classList.toggle("show");

    }
);