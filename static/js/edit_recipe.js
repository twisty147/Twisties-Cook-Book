document.addEventListener('DOMContentLoaded', function () {
    // Set initial counts based on existing fields, ensuring fallback to 0 if not present.
    let ingredientCount = parseInt("{{ recipe.ingredients|length }}", 10) || 0;
    let stepCount = parseInt("{{ recipe.preparation_steps|length }}", 10) || 0;
    let toolCount = parseInt("{{ recipe.required_tools|length }}", 10) || 0;

    // Add Ingredient
    document.getElementById('add-ingredient-btn').addEventListener('click', function () {
        ingredientCount++; // Increment the ingredient counter correctly
        const newIngredient = `
            <div class="input-field" style="display: flex;" id="ingredient-${ingredientCount}">
                <input type="text" id="ingredient_input_${ingredientCount}" name="ingredients[]" required>
                <label for="ingredient_input_${ingredientCount}">Ingredient </label>
                <i class="material-icons red-text delete-ingredient" style="cursor: pointer;">delete</i>
            </div>`;
        document.getElementById('ingredients-section').insertAdjacentHTML('beforeend', newIngredient);
    });

    // Add Preparation Step
    document.getElementById('add-step-btn').addEventListener('click', function () {
        stepCount++; // Increment the step counter correctly
        const newStep = `
            <div class="input-field" style="display: flex;" id="step-${stepCount}">
                <textarea id="preparation_step_${stepCount}" name="preparation_steps[]" class="materialize-textarea" required></textarea>
                <label for="preparation_step_${stepCount}">Step ${stepCount}</label>
                <i class="material-icons red-text delete-step" style="cursor: pointer;">delete</i>
            </div>`;
        document.getElementById('preparation-steps-section').insertAdjacentHTML('beforeend', newStep);
    });

    // Add Required Tool
    document.getElementById('add-tool-btn').addEventListener('click', function () {
        toolCount++; // Increment the tool counter correctly
        const newTool = `
        <div class="input-field" style="display: flex;" id="tool-${toolCount}">
            <input type="text" id="required_tool_${toolCount}" name="required_tools[]" required>
            <label for="required_tool_${toolCount}">Tool ${toolCount}</label>
            <i class="material-icons red-text delete-tool" style="cursor: pointer;">delete</i>
        </div>`;
        document.getElementById('required-tools-section').insertAdjacentHTML('beforeend', newTool);
    });

    // Delete Ingredient
    document.getElementById('ingredients-section').addEventListener('click', function (e) {
        if (e.target.classList.contains('delete-ingredient')) {
            e.target.parentElement.remove();
            ingredientCount--; // Adjust the count when an item is deleted
        }
    });

    // Delete Preparation Step
    document.getElementById('preparation-steps-section').addEventListener('click', function (e) {
        if (e.target.classList.contains('delete-step')) {
            e.target.parentElement.remove();
            stepCount--; // Adjust the count when an item is deleted
        }
    });

    // Delete Required Tool
    document.getElementById('required-tools-section').addEventListener('click', function (e) {
        if (e.target.classList.contains('delete-tool')) {
            e.target.parentElement.remove();
            toolCount--; // Adjust the count when an item is deleted
        }
    });
});
