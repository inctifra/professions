export default async function deleteDomain() {
    const {default: $ } = await import("jquery");
    const {default: axiosInstance} = await import("../../../libs/main");


$("tr.table-domains-row").each(function () {
    const element = $(this);
    const deleteUrl = element.data("delete-url");
    element.find("button").on("click", async function () {
        try {
            const response = await axiosInstance.post(deleteUrl);
            if (response.data.has_keys) {
                const confirmDelete = confirm(response.data.message);
                if (!confirmDelete) return;
                await axiosInstance.post(deleteUrl + "?force=1"); 
            }
            if (response.data.success) {
                alert(response.data.message);
                element.remove();
            }
        } catch (error) {
            console.error("Delete failed", error.response?.data || error);
            alert("Failed to delete domain. See console for details.");
        }
    });
});


}

deleteDomain()