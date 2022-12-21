

const submit = document.querySelector('#upload-form');
const uploadFeedback = document.querySelector('.invalid-upload');
const displayProbability = document.querySelector('.display-probability')

// const messages = document.querySelector('.messages');
submit.addEventListener('submit', (e) => {
    console.log('e', e);
    e.preventDefault();
    const fileVal = e.target.elements['id_file'].value;
    uploadFeedback.style.display = 'none';
    displayProbability.style.display = 'none';

    if(fileVal) {
        if(fileVal.substr(fileVal.length - 5) == ".json") {
            const form_data = new FormData();
            const file = document.getElementById('id_file').files[0]
            form_data.append("file", file);

            // console.log(form_data)
            // csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
            // coneols.log(csrf_token)
            // submit.submit()
            fetch('/', {
                method: 'POST',
                mode: 'same-origin',  
                headers:{
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest', 
                },
                body: form_data,
            })        
            .then(response => response.json())
            .then(data => {
                var probability_success = data['probability_success']
                displayProbability.style.display = 'block';   
                displayProbability.innerHTML = `<h3>The Probability of Success is ${probability_success}</h3>`;
            })
        }
        else {
            uploadFeedback.style.display = 'block';
            uploadFeedback.innerHTML = `<p>Please upload a json file</p>`;
        }
    } 
    else {
        uploadFeedback.style.display = 'block';
        uploadFeedback.innerHTML = `<p>Please upload a file</p>`;  
    }

})
