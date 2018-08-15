<template>
    <div class="table-layout">
        <div class="table-cell document-thumbnail hidden-xs">
            <!-- <img :src="doc.thumbnail_url"> -->
        </div>
        <div class="table-cell document-body">
            <p class="title">{{data.title}}</p>
            <div>
                <p><span>Autor:</span>{{data.author}}</p>
                <p><span>Fecha de publicación:</span>{{data.creation_date}}</p>
                <p><span>Páginas:</span>{{data.pages}}</p>
                <p><span>Tamaño:</span>{{data.size}}</p>
                <p><span>Subido:</span>{{data.upload_date}}</p>
            </div>
        </div>
        <div class="table-cell document-file">
            <a :href="data.file_url" download="">PDF</a>
        </div>
    </div>
</template>

<script>
export default {
    name: 'DocumentGridView',
    props: {
        data: {
            type: Object,
            required: true
        }
    },
    data() {
        return {}
    }
}
</script>

<style>
.table-layout {
    display: table;
    width: 100%;
    margin: 15px 0;
}

.table-layout .table-cell {
    display: table-cell;
    border: solid 1px #ccc;
    vertical-align: top;
}

.document-file {
    width: 100px;
}

.document-thumbnail,
.document-thumbnail>img {
    width: 110px;
}

.document-body {
    padding: 0 5px;
}

.document-body p {
    margin: 0;
}
</style>
