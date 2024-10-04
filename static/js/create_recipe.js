
document.addEventListener('DOMContentLoaded', function () {
    let ingredientCount = 1;
    let stepCount = 1;
    let toolCount = 1;
    // Add Ingredient
    document.getElementById('add-ingredient-btn').addEventListener('click', function () {
        ingredientCount++;
        const newIngredient = `
            <div class="input-field" id="ingredient-${ingredientCount}" style="display: flex;">
                <input type="text" id="ingredient_input_${ingredientCount}" name="ingredients[]" required>
                <label for="ingredient_input_${ingredientCount}">Ingredient </label>
                <i class="material-icons red-text delete-ingredient" style="cursor: pointer;">delete</i>
            </div>`;
        document.getElementById('ingredients-section').insertAdjacentHTML('beforeend', newIngredient);
    });
    // Add Preparation Step
    document.getElementById('add-step-btn').addEventListener('click', function () {
        stepCount++;
        const newStep = `
            <div class="input-field" id="step-${stepCount}" style="display: flex;">
                <textarea id="preparation_step_${stepCount}" name="preparation_steps[]" class="materialize-textarea" required></textarea>
                <label for="preparation_step_${stepCount}">Step ${stepCount}</label>
                <i class="material-icons red-text delete-step" style="cursor: pointer;">delete</i>
            </div>`;
        document.getElementById('preparation-steps-section').insertAdjacentHTML('beforeend', newStep);
    });
    // Delete Ingredient
    document.getElementById('ingredients-section').addEventListener('click', function (e) {
        if (e.target.classList.contains('delete-ingredient')) {
            e.target.parentElement.remove();
        }
    });
    // Delete Preparation Step
    document.getElementById('preparation-steps-section').addEventListener('click', function (e) {
        if (e.target.classList.contains('delete-step')) {
            e.target.parentElement.remove();
        }
    });
    // Add Required Tool
    document.getElementById('add-tool-btn').addEventListener('click', function () {
        toolCount++;
        const newTool = `
    <div class="input-field" id="tool-${toolCount}" style="display: flex;">
        <input type="text" id="tool_input_${toolCount}" name="required_tools[]" required>
        <label for="tool_input_${toolCount}">Tool ${toolCount}</label>
        <i class="material-icons red-text delete-tool" style="cursor: pointer;">delete</i>
    </div>`;
        document.getElementById('tools-section').insertAdjacentHTML('beforeend', newTool);
    });
    // Delete Required Tool
    document.getElementById('tools-section').addEventListener('click', function (e) {
        if (e.target.classList.contains('delete-tool')) {
            e.target.parentElement.remove();
        }
    });
});