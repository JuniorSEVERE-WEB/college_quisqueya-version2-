document.addEventListener("DOMContentLoaded", function () {
    const programSelect = document.getElementById("id_program");
    const classroomSelect = document.getElementById("id_classroom");

    function filterClassrooms() {
        const programId = programSelect.value;

        // Cache toutes les options sauf celles du bon program
        Array.from(classroomSelect.options).forEach(option => {
            if (!option.value) return; // garde le vide
            const program = option.textContent.match(/\((.*?)\)$/); // extrait le nom du programme
            if (program && program[1]) {
                option.style.display = (program[1] === programSelect.options[programSelect.selectedIndex].text) ? "block" : "none";
            }
        });

        // Réinitialise la sélection
        classroomSelect.value = "";
    }

    if (programSelect) {
        programSelect.addEventListener("change", filterClassrooms);
        filterClassrooms(); // exécute au chargement
    }
});
