function showForm(formId) {
    // Masquer tous les formulaires
    const forms = document.getElementsByClassName('form-container');
    for (let form of forms) {
        form.style.display = 'none';
    }

    // Afficher le formulaire sélectionné
    document.getElementById(formId).style.display = 'block';
}
