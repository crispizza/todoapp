<template lang="pug">
div
    h1 todo list
    div
        input(type="text" placeholder="task name" v-model="input_task" @keyup.enter="create(input_task)")
        button(@click="create(input_task)") add
    div
        ul
            li(v-for="(item,index) in tasks")
                input(type="checkbox" v-model="item.done" @change="update(item)")
                span {{item.task}}
                span.pointer(@click="remove(item, index)") 🗑

</template>
<script>
import axios from "axios";
export default {
    data: () => ({
        input_task: "",
        tasks:[]
    }),
    created() {
        this.readAll();
    },
    methods: {
        create(item) {
            if(!item) return;
            axios.post("http://18.181.97.237:80/task",{task:this.input_task})
            .then((response) => {
                const data = response.data
                this.tasks.push({
                    _id: data["LAST_INSERT_ID()"],
                    task: this.input_task,
                    done: 0
                });
                this.input_task = "";
            })
            .catch((error) => {
                console.error(error);
            });
        },
        readAll() {
            axios.get("http://18.181.97.237:80/task")
                .then((response) =>
                    response.data.forEach((data) =>
                        this.tasks.push({
                            _id: data._id,
                            task: data.task,
                            done: data.done
                        })
                    )
                )
                .catch((error) => {
                    console.error(error);
                });
        },
        update(item) {
            axios.put("http://18.181.97.237:80/task",{_id: item._id, done: item.done})
                .catch((error) => {
                    console.error(error);
                });
        },
        remove(item, index) {
            axios.delete("http://18.181.97.237:80/task",{params: {_id: item._id}})
                .then(() => {
                    this.tasks.splice(index,1);
                })
                .catch((error) => {
                    console.error(error);
                });
        }
    }
}
</script>
<style scoped>
ul, li {
    list-style: none;
    font-weight: bold;
}
.pointer {
    cursor: pointer;
}
</style>
