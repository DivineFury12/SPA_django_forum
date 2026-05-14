const elementById = document.getElementById('my_element');
if (elementById) {
    console.log('Text by ID:', elementById.textContent);
    
    const newElement = document.createElement('h2');
    
    newElement.textContent = elementById.textContent;
    
    newElement.style.marginTop = '10px';
    elementById.insertAdjacentElement('afterend', newElement);
}

const toggleButton = document.createElement('button');
toggleButton.textContent = 'Показать/Скрыть форму';
toggleButton.style.margin = '20px';
toggleButton.style.padding = '10px 20px';
toggleButton.style.backgroundColor = '#2196F3';
toggleButton.style.color = 'white';
toggleButton.style.border = 'none';
toggleButton.style.borderRadius = '4px';
toggleButton.style.cursor = 'pointer';
toggleButton.style.fontSize = '16px';

const form = document.createElement('form');
form.style.margin = '20px';
form.style.padding = '20px';
form.style.backgroundColor = '#f5f5f5';
form.style.borderRadius = '8px';

form.style.display = 'none';

const input = document.createElement('input');
input.type = 'text';
input.placeholder = 'Введите число';
input.style.padding = '10px';
input.style.marginRight = '10px';
input.style.border = '1px solid #ddd';
input.style.borderRadius = '4px';
input.style.fontSize = '16px';
input.style.width = '200px';

const button = document.createElement('button');
button.textContent = 'Отправить';
button.style.padding = '10px 20px';
button.style.backgroundColor = '#4CAF50';
button.style.color = 'white';
button.style.border = 'none';
button.style.borderRadius = '4px';
button.style.cursor = 'pointer';
button.style.fontSize = '16px';

button.addEventListener('click', (e) => {
    e.preventDefault();
    const value = input.value.trim();
    
    if (value === '') {
        alert('Пожалуйста, введите число');
        return;
    }
    
    if (isNaN(value)) {
        alert('Ошибка: Введите корректное число');
    } 
    else {
        alert('Отлично! Вы ввели число: ' + value);
    }
});

toggleButton.addEventListener('click', () => {
    if (form.style.display === 'none') {
        form.style.display = 'block';
    }
    else {
        form.style.display = 'none';
        input.value = '';
    }
});

form.appendChild(input);
form.appendChild(button);

document.body.appendChild(toggleButton);
document.body.appendChild(form);

