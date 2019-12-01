// get DOM
let code_html, string_html, dom_html, style_none, img_pos;
let content = document.getElementById("content_edit");
let freeze_panel = document.getElementsByClassName("freeze");
let download_file = document.getElementById("download_file");
let title_file = document.getElementById('title_file');

let code = document.getElementById("code_edit");
let undo = document.getElementById("undo");
let redo = document.getElementById("redo");

let text_center = document.getElementById("justifyCenter");
let text_left = document.getElementById("justifyLeft");
let text_right = document.getElementById("justifyRight");
let text_justify = document.getElementById("justifyFull");

let text_italic = document.getElementById("italic");
let text_bold = document.getElementById("bold");
let text_paragraph = document.getElementById("paragraph");
let text_blockquote = document.getElementById("blockquote");
let text_underline = document.getElementById("underline");
let remove_format = document.getElementById("removeFormat");

let head_h1 = document.getElementById("h1");
let head_h2 = document.getElementById("h2");
let head_h3 = document.getElementById("h3");
let head_h4 = document.getElementById("h4");

let font_name = document.getElementById("fontName");
let font_size = document.getElementById("fontSize");

let color_piker = document.getElementById("colorPicker");

let add_indent = document.getElementById("indent");
let out_indent = document.getElementById("outdent");

let list_ol = document.getElementById("insertOrderedList");
let list_ul = document.getElementById("insertUnorderedList");

let create_link = document.getElementById("createLink");
let un_link = document.getElementById("unlink");

let url_image = document.getElementById("insertImage");
let user_tag = document.getElementById("userTag");

let clear_message = document.getElementById("clear_message");

// undo & redo
undo.onclick = () => formatDoc(undo.id);
redo.onclick = () => formatDoc(redo.id);

//heading format
head_h1.onclick = () => formatDoc('formatBlock', head_h1.id);
head_h2.onclick = () => formatDoc('formatBlock', head_h2.id);
head_h3.onclick = () => formatDoc('formatBlock', head_h3.id);
head_h4.onclick = () => formatDoc('formatBlock', head_h4.id);

text_bold.onclick = () => formatDoc(text_bold.id);
text_italic.onclick = () => formatDoc(text_italic.id);
text_paragraph.onclick = () => formatDoc('formatBlock', text_paragraph.id);
text_blockquote.onclick = () => formatDoc('formatBlock', text_blockquote.id);
text_underline.onclick = () => formatDoc(text_underline.id);
remove_format.onclick = () => formatDoc(remove_format.id);

//position
text_center.onclick = () => formatDoc(text_center.id);
text_left.onclick = () => formatDoc(text_left.id);
text_right.onclick = () => formatDoc(text_right.id);
text_justify.onclick = () => formatDoc(text_justify.id);

//indent & out dent
add_indent.onclick = () => formatDoc(add_indent.id);
out_indent.onclick = () => formatDoc(out_indent.id);

//list ol & list ui
list_ol.onclick = () => formatDoc(list_ol.id);
list_ul.onclick = () => formatDoc(list_ul.id);

user_tag.onclick = () => formatDoc('insertHTML', "<recipient>Name</recipient>");

url_image.addEventListener("click", function () {
    title_file.innerText = 'Download image';
    img_pos = dom_html;
    $('#add_file').modal('show');
});
// selectAll , delete

clear_message.addEventListener("click", function () {
    let message = document.getElementById('message_html');
    message.setAttribute('contentEditable', true);
    message.focus();
    formatDoc("selectAll", false);
    formatDoc("delete", false);
    message.removeAttribute('contentEditable');

});


download_file.addEventListener("click", function () {
    let url_file = document.getElementById('url').value;
    let width_file = document.getElementById('width').value;
    let height_file = document.getElementById('height').value;

    if (url_file !== '' && img_pos !== undefined) {
        download_image(url_file, width_file, height_file);
    }
    $('#add_file').modal('hide');
});


function download_image(url, width, height) {
    let img = document.createElement('img');
    img.src = url;
    if (width !== '') {
        img.width = width;
    }
    if (height !== '') {
        img.height = height;
    }
    img_pos.appendChild(img);

}

content.onclick = function (e) {
    dom_html = e.target;
    let file_attach = document.getElementById("file");
    if (style_none) {
        style_none.removeAttribute('contentEditable');

    }
    if (dom_html.id !== "content_edit" && dom_html.id !== "message_html") {
        if (dom_html.id !== "message" && dom_html !== file_attach) {
            if (dom_html !== file_attach.parentNode) {
                style_none = dom_html;
                style_none.contentEditable = "true";
                style_none.focus();
                console.log(style_none)
            }
        }
    }
};

color_piker.addEventListener("input", function () {
    let hex = color_piker.value;
    if ('' !== window.getSelection().toString()) {
        formatDoc("foreColor", hex);
    } else {
        if (dom_html.id !== 'content_edit') {
            let bg_color = 'background:' + hex;
            dom_html.setAttribute('style', bg_color);
        }
    }

}, false);


font_name.addEventListener("click", function (e) {
    let font = font_name.getElementsByClassName('a');
    let font_index = [].indexOf.call(this.children, (e ? e.target : event.srcElement));
    formatDoc(font_name.id, font[font_index].textContent);
});

font_size.addEventListener("click", function (e) {
    let font_size_index = [].indexOf.call(this.children, (e ? e.target : event.srcElement));
    formatDoc(font_size.id, font_size_index + 1);
});

create_link.addEventListener("click", function () {
    let sLnk = prompt('Введите ваш URL', 'http:\/\/');
    if (sLnk && sLnk !== '' && sLnk !== 'http://') {
        formatDoc(create_link.id, sLnk)
    }
});

un_link.onclick = () => formatDoc(un_link.id);

function formatDoc(sCmd, sValue) {
    document.execCommand(sCmd, false, sValue);
    content.focus();
}

//convert string to html
code.addEventListener('click', function () {
    code_html = document.getElementById("message_html");
    string_html = document.getElementById("message_string");

    if (code_html) {
        code.style.color = '#ec1c21';
        freeze_but(freeze_panel, 'none');
        console.log("convert to string!");
        code_html.innerText = code_html.innerHTML.toString();
        code_html.id = "message_string";

    } else {
        code.style.color = '#6c757d';
        freeze_but(freeze_panel, 'block');
        console.log("convert to html!");
        string_html.innerHTML = string_html.innerText;
        string_html.id = "message_html";

    }

});

//upload read file html
// document.querySelector('#file-upload').onchange = function () {
//     let file = this.files[0];
//     let reader = new FileReader();
//     reader.onload = function () {
//         document.getElementById('message').innerHTML = reader.result;
//     };
//     reader.readAsText(file)
// };

function freeze_but(array_elem, param_block) {
    for (let i = 0; i < array_elem.length; i++) {
        freeze_panel[i].style.display = param_block;
        console.log(freeze_panel[i], param_block);
    }
}
