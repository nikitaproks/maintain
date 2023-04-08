import { redirect } from "@sveltejs/kit"
import { requireAuth } from '../../middleware';



export async function load({ fetch, request }) {

    const authData = await requireAuth(fetch, request);

    if (!authData.email) throw redirect(303, '/login')
    return { authData };
}