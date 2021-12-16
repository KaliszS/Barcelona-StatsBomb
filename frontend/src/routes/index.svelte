<script>
    import { onMount } from "svelte";

    const endpoint = "http://localhost:8899/competition";
    let competitions = [];
    
    onMount(async function () {
        const response = await fetch(endpoint);
        const data = await response.json();
        console.log(data);
        competitions = data;
    });
</script>

<main>

    {#each competitions as comp}
        <div class="list">
            <p>{comp.competition_name} [{comp.season_name}]</p>
        </div>
    {/each}
</main>

<style>
.list {
    display: flex;
    margin: 10px;
    border: 5px solid black;
}
</style>