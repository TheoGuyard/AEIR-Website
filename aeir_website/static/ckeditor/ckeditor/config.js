/**
 * @license Copyright (c) 2003-2019, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function(config) {
  config.toolbarGroups = [
    { name: "basicstyles", groups: ["basicstyles", "cleanup"] },
    {
      name: "paragraph",
      groups: ["list", "indent", "blocks", "align", "bidi", "paragraph"]
    },
    { name: "styles", groups: ["styles"] },
    { name: "colors", groups: ["colors"] }
  ];

  config.removeButtons =
    "Underline,Subscript,Superscript,Cut,Undo,Scayt,Link,Image,Maximize,Source,About";
};

