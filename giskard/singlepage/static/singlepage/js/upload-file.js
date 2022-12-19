

const submit = document.querySelector('#upload-form');
const uploadFeedback = document.querySelector('.invalid-upload');

// const messages = document.querySelector('.messages');
submit.addEventListener('submit', (e) => {
    console.log('e', e);
    e.preventDefault();
    const fileVal = e.target.elements['id_file'].value;
    uploadFeedback.style.display = 'none';

    if(fileVal) {
        if(fileVal.substr(fileVal.length - 5) == ".json") {
            submit.submit()
            // fetch('render/', {
            //     body: JSON.stringify({empire_file : fileVal}),
            //     method: "POST",
            // })        
            // .then(response => response.json())
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
