let translation_area = document.getElementById("translation_area");
var response = [];
let english_word;


translation_area.addEventListener('keyup', function translate(e) {
    document.getElementById('hindi_words_list').style.display = 'none';
    if (e.keyCode == 32) {

        let text_value = translation_area.value;
        //        let trimmed_text_value = text_value.trim();

        var words = text_value.split(' ');
        var lastWord = words[words.length - 2];
        english_word = lastWord;

        if (english_word != '') {
            fetch(`/v1/translate?query=${lastWord}`)
                .then(res => res.json())
                .then(data => {
                    console.log(data.data)
                    response = data.data;

                    var high_score_word = response[0];

                    translation_area.value = text_value.substring(0, text_value.length - english_word.length - 1) + high_score_word + " ";

                })
                .catch(error => console.log('ERROR'))
        }
    }

    if (e.keyCode == 8) {
        var x = event.screenX;
        var y = event.screenY;
        console.log(x);
        console.log(y);

        document.getElementById('hindi_words_list').style.display = 'block';
        //        document.getElementById('hindi_words_list').style.left=200px;
        //        document.getElementById('hindi_words_list').style.top=300px;
        var str = '<select id="translation_options_dropdown" onchange="change_hindi()">';
        for (let i = 0; i < response.length; i++) { str += '<option>' + response[i] + '</option>'; }
        str += '<option>' + english_word + '</option>';
        str += '</select>';



        var el = document.getElementById("translation_area");
        //        console.log(el.getBoundingClientRect());


        document.getElementById("hindi_words_list").innerHTML = str;

    }

});


function change_hindi() {

    var x = document.getElementById("translation_options_dropdown").value;
    const textarea = document.getElementById('translation_area');
    textarea.value = textarea.value.replace(/\w+$/, ' ');
    textarea.value = textarea.value.substring(0, textarea.value.lastIndexOf(' ')) + ' ' + x + ' ';
    document.getElementById('hindi_words_list').style.display = 'none';

    //    $("#hindi_words_list").css({ 'top': 200, 'left': 600 });

    //    document.getElementById("hindi_words_list").style.top = "200px";

};