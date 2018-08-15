<template>
  <el-dialog class="upload-component" :title="dialogTitle" :closeOnPressEscape="false" :visible.sync="isUploading" width="500px" :close-on-click-modal="false" :before-close="closeDialog">
    <el-upload ref="upload" :on-change="change" :on-remove="removeFile" drag :auto-upload="false" v-bind:class="{'has-files':hasFiles}" :http-request="uploadDocument" action="none">
      <div v-if="!hasFiles">
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">Suelta tu archivo aquí o
          <em>haz clic para cargar</em>
        </div>
        <div slot="tip" class="el-upload__tip">Solo archivos
          <strong>pdf</strong> con un tamaño menor de
          <strong>200MB</strong>
        </div>
      </div>
    </el-upload>
    <el-button v-if="hasFiles" size="small" class="send" type="success" @click="submitUpload">
      <i class="el-icon-upload"></i> Enviar al servidor
    </el-button>
    <div v-loading="uploading"></div>
  </el-dialog>
</template>
<script>
import { mapGetters, mapActions } from 'vuex';
import coreServices from '@/services/core';

export default {
  data() {
    return {
      hasFiles: false,
      dialogTitle: "Añadir nuevo documento",
      uploading: false,
    }
  },
  methods: {
    ...mapActions([
      'setUploading'
    ]),
    closeDialog(done) {
      this.setUploading(false);
      this.$refs.upload.abort();
      this.$refs.upload.clearFiles();
      this.hasFiles = false;
    },
    submitUpload() {
      this.$refs.upload.submit();
    },
    uploadDocument(requestData) {
      let formData = new FormData();
      formData.append('document', requestData.file);
      this.uploading = true;
      coreServices.uploadDocument(formData)
        .then(response => {
          console.info(response.data);
          this.uploading = false;
        }, (error) => {
          if (error.data) {
            console.info(error.data.message)
          }
          this.uploading = false;
        })
    },
    errorUploding(error) {
      console.info('error al subir el archivo')
    },
    removeFile(file, fileList) {
      this.hasFiles = fileList.length > 0
    },
    change: function(file, fileList) {
      this.hasFiles = fileList.length > 0
    }
  },
  computed: {
    ...mapGetters([
      'isUploading'
    ])
  }
}
</script>

<style>
.el-upload-list__item {
  background-color: #f5f7fa;
}

.has-files .el-upload {
  display: none;
}

.el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 4px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  min-width: 100%;
}

.el-upload-dragger {
  border: none;
  margin: 0 auto;
}

.el-upload-dragger .el-icon-upload {
  margin: 30px 0 16px;
}

.el-upload:hover,
.el-upload:focus {
  border-color: #409EFF;
}

.upload-component .el-dialog__body {
  padding: 15px 20px 20px;
}

button.send {
  margin-top: 20px;
}
</style>
