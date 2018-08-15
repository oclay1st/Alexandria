<template>
    <div class="search-component">
        <el-form class="simple-search" ref="form">
            <el-form-item>
                <el-input v-bind:size="size"  :class="{searching: criteria}" v-model="criteria" @keyup.enter="clickSearch(criteria)" placeholder="Despliega tu imaginacion">
                    <i v-if="criteria" slot="suffix" @click="clickClean" class="el-input__icon el-icon-close"></i>
                    <el-button class="search-button" slot="append" @click="clickSearch(criteria)" icon="el-icon-search"></el-button>
                </el-input>
                <ul class="search-dropdown show" v-if="suggestions.length" v-on-click-outside="outside">
                    <li class="dropdown-menu-item" @click="clickItem(suggestion)" v-for="(suggestion,index) in suggestions" :key='index' role="menu-item">
                        {{suggestion}}
                    </li>
                </ul>
            </el-form-item>
            <el-form-item v-show='hasAdvanced'>
                <el-button icon='more' @click="advanced=!advanced"></el-button>
            </el-form-item>

        </el-form>
        <!--Advanced-->
        <el-form class="advanced-form" v-if="advanced" :label-position="labelPosition" ref="form" :model="advancedForm">
            <el-row :gutter="10">
                <el-col :xs="24" :sm="8">
                    <el-form-item label="con la frase exacta">
                        <el-input v-model="advancedForm.frase"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :xs="24" :sm="8">
                    <el-form-item label="sin las palabras">
                        <el-input v-model="advancedForm.frase"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :xs="24" :sm="8">
                    <el-form-item label="con  el idioma">
                        <el-input v-model="advancedForm.frase"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :xs="24" :sm="8">
                    <el-form-item label="con el nombre autor">
                        <el-input v-model="advancedForm.frase"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :xs="24" :sm="8">
                    <el-form-item label="con fecha de subida">
                        <el-input v-model="advancedForm.frase"></el-input>
                    </el-form-item>
                </el-col>
            </el-row>
        </el-form>
    </div>
</template>
<script>
import { mixin as onClickOutside } from 'vue-on-click-outside';
import coreServices from '@/services/core';
import lodash from 'lodash';
import http from '@/config/http';
export default {
    name: 'SearchDocument',
    mixins: [onClickOutside],
    props: {
        clickSearch: {
            type: Function,
            default: () => { }
        },
        hasAdvanced: {
            type: Boolean,
            default: false
        },
        size: {
            type: String,
            default: 'small'
        }

    },
    data() {
        return {
            labelPosition: 'top',
            suggestions: [],
            advancedForm: {
                frase: ''
            },
            criteria: '',
            searchForm: {},
            advanced: false,
            autocomplete: true
        }
    },
    methods: {
        seachSuggestons:
        _.debounce(function() {
            var vm = this;
            if (this.criteria && this.autocomplete) {
                coreServices.getSuggestions({ params: { 'criteria': this.criteria } })
                    .then((response) => {
                        vm.suggestions = response.data.suggestions
                    }).catch((response) => {
                        console.info('error')
                    })
            } else {
                vm.autocomplete = true;
                vm.suggestions = []
            }
        }, 500
        ),
        clickItem(suggestion) {
            this.criteria = suggestion;
            this.suggestions = [];
            this.autocomplete = false;
            this.clickSearch(suggestion)
        },
        clickClean() {
            this.criteria = ''
        },
        outside() {
            this.suggestions = []
        },
        onHover() {
            console.info('hi')
        }
    },
    watch: {
        criteria: function() {
            this.seachSuggestons()
        }
    }
}
</script>
<style>
.search-component .search-dropdown {
    background-color: #fff;
    border: 1px solid #d1dbe5;
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .12);
    padding: 6px 0;
    z-index: 10;
    position: absolute;
    top: 37px;
    width: 100%;
}

.search-component .dropdown-menu-item {
    list-style: none;
    line-height: 36px;
    padding: 0 10px;
    margin: 0;
    cursor: pointer
}

.search-component .dropdown-menu-item:hover {
    background-color: #e4e8f1;
    color: #48576a;
}

.advanced-form label.el-form-item__label {
    padding: 0;
}

.advanced-form {
    margin-top: 10px;
}

.searching i.el-icon-close {
    cursor: pointer;
}
</style>
