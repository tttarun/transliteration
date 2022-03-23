
let translation_area = document.getElementById("translation_area");
var response = [];
let english_word;
let len;
var selected_key;
var dict={};
var words_array =[];
var st,e,l;


translation_area.addEventListener('keyup',function translate(e) {
    document.getElementById('hindi_words_list').style.display='none';
    if(e.keyCode == 32){

        let text_value = translation_area.value;
//        let trimmed_text_value = text_value.trim();

        var words = text_value.split(' ');
        var lastWord = words[words.length - 2];
        english_word=lastWord;

        let reversed = "";
        let str=english_word;
        let flag=true;
          for (var i = str.length - 1; i >= 0; i--){
              if ((str[i]>='a' && str[i]<='z') || (str[i]>='A' && str[i]<='Z'))
              {
                  reversed+=str[i];
              }else
              {  flag=false;
                 reversed=ReverseString(reversed);
                 break;
              }
          }
          function ReverseString(s) {return s.split("").reverse().join("");}
          if (flag){
          english_word=str;}
          else
          {
              english_word=reversed;
          }

        if (english_word!='')
{
        fetch(`/v1/translate?query=${english_word}`)
        .then(res=> res.json())
        .then(data =>{
        console.log(data.data)
        response = data.data;

        var high_score_word= response[0];

        len=high_score_word.length;

        selected_key=high_score_word;
        words_array=response;
        words_array.unshift(english_word);

        dict[selected_key]=words_array;


        translation_area.value = text_value.substring(0,text_value.length- english_word.length -1) + high_score_word + " " ;

        })
        .catch(error => console.log('ERROR'))
      }
      }

    if(e.keyCode == 8){
    try{
        console.log(dict);

        let translation_area = document.getElementById("translation_area");
        let text_value = translation_area.value;
        console.log(text_value);

        var myElement = document.getElementById('translation_area');
        var startPosition = myElement.selectionStart;
        var endPosition = myElement.selectionEnd;
        window.gs=startPosition;
        window.ge=endPosition;
        console.log(startPosition)
        console.log(endPosition)

        t=text_value.slice(0,startPosition)
        a=t.split(' ')
        l=a[a.length-1]
        l=l.trim()
        list=dict[l]
//        window.hin_len=l.length
        window.eng_len=list[0].length
        var tt=0;
        if (startPosition >185)
        {
        tt=Math.floor(startPosition/185);
        startPosition=startPosition%185;

        }
        console.log("tt=",tt);

        document.getElementById('hindi_words_list').style.left=startPosition*5.25+400+'px';
        document.getElementById('hindi_words_list').style.top=(tt*20)+250+'px';



        document.getElementById('hindi_words_list').style.display='block';
        var str = '<select id="translation_options_dropdown" onclick="change_hindi()" onkeypress="change_hindi()">';
       for (let i = 0; i < list.length; i++)
       { str += '<option>'+ list[i] + '</option>';}
        str += '</select>';

        var el=document.getElementById("translation_area");


        document.getElementById("hindi_words_list").innerHTML = str;

        var x = document.getElementById("translation_options_dropdown").value;
        const textarea = document.getElementById('translation_area');
        textarea.value = replaceRange(textarea.value, gs-l.length, gs, dict[l][0]+' ');
        window.el=dict[l][0].length



        var dropdown = document.getElementById("translation_options_dropdown");
        dropdown.focus();
        dropdown.size = dropdown.options.length;

        if (eng_len>list[1].length)
        {
        gs=gs+(eng_len-list[1].length);
        }else if(eng_len<list[1].length)
        {
        gs=gs-(list[1].length-eng_len);
        }
}catch(err)
{

}


        }


});


//function change_hindi() {
//
//    var x = document.getElementById("translation_options_dropdown").value;
//    const textarea = document.getElementById('translation_area');
//    s=translation_area.value;
//    textarea.value = textarea.value.replace(/\w+$/, ' ');
//    textarea.value = textarea.value.substring(0, textarea.value.lastIndexOf(' ')) +' '+x+' ';
//    document.getElementById('hindi_words_list').style.display='none';
//
//
//};

function change_hindi() {

    var x = document.getElementById("translation_options_dropdown").value;
    const textarea = document.getElementById('translation_area');
    var s=translation_area.value;
    var sp=s.split(' ');
    var hin_len=x.length;

    var select = document.getElementById('translation_options_dropdown'),
    opts = select.getElementsByTagName('option'),
    x_list = [];

    for (var i = 0, len = opts.length; i < len; i++) {
    x_list.push(opts[i].value);
        }

    dict[x]=x_list;


    if(sp[sp.length-1].startsWith('\n'))
    {
    textarea.value = textarea.value.substring(0, textarea.value.lastIndexOf('')-len) +x+' ';
    window.len=x.length;
    }else
    {
//    textarea.value = textarea.value.substring(0, textarea.value.lastIndexOf(' ')) +' '+x+' ';
      console.log(s);
      textarea.value = replaceRange(textarea.value, gs-eng_len, gs, x);

    }

    document.getElementById('hindi_words_list').style.display='none';
    var text_focus = document.getElementById("translation_area");
    text_focus.focus();


};

function replaceRange(s, start, end, substitute) {
    return s.substring(0, start) + substitute + s.substring(end);
};


//let submit_button = document.getElementById("submit_button");
//
//submit_button.addEventListener('onclick',function() {
//document.getElementById('lll').style.display='none';
//}
//);

function submit_button()
{
document.getElementById("lll").style.display='block';
}



