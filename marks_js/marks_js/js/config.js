// ========== SUPABASE CONFIG ==========
// 1. Create project at https://supabase.com
// 2. Project Settings → API → copy URL and anon key
// 3. Paste them below

const SUPABASE_URL ='https://xtzimhjzjxcovogxncbf.supabase.co';       // e.g. https://xxxx.supabase.co
const SUPABASE_ANON_KEY ='sb_publishable_23OkEdsWDacweEitLTOCcw_lA_08NBZ';

// Create client (loaded from CDN in HTML)
let supabase = null;

function initSupabase() {
  if (typeof window.supabase !== 'undefined' && SUPABASE_URL !== 'YOUR_SUPABASE_URL') {
    supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
    return true;
  }
  return false;
}
