<template>
    <div class="table-layout">
            <div class="table-cell document-thumbnail hidden-xs">
                <img alt="doc.title" src="doc.thumbnail_url"/>
            </div>
            <div class="table-cell document-body">
                <div>
                    <p>{{doc.summary}}</p>
                </div>
            </div>
            <div class="table-cell document-file">
                <a href="doc.file_url" download>PDF</a>
            </div>
        </div>
</template>

<script>
    export default{
        name:'DocumentDetailsView',
        props:{
            doc:{
                type:Object,
                required:true,
                default:{}
            }
        },
        data (){
            return {
                data:{}
            }
        }
    }
</script>

<style>
    .table-layout {
        display:table;
        width:100%;
        margin:15px 0;
    }
    .table-layout .table-cell {
        display:table-cell;
        border:solid 1px #ccc;
        vertical-align: top;
    }
    .document-file{
        width:100px;
    }
    .document-thumbnail,.document-thumbnail >img {
        width:110px;
    }
    .document-body{
        padding:0 5px;
    }
    .document-body p{
        margin: 0;
    }
</style>
