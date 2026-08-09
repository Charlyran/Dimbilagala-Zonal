// ========== SUPABASE CONFIG ==========
// Paste your keys from Supabase → Project Settings → API
const SUPABASE_URL = 'https://xtzimhjzjxcovogxncbf.supabase.co';
const SUPABASE_ANON_KEY = 'sb_publishable_23OkEdsWDacweEitLTOCcw_lA_08NBZ';

// Demo mode = true when keys not set (preview without database)
const DEMO_MODE = (SUPABASE_URL === 'https://xtzimhjzjxcovogxncbf.supabase.coL');

let supabase = null;

function initSupabase() {
  if (!DEMO_MODE && typeof window.supabase !== 'undefined') {
    supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
    return true;
  }
  return !DEMO_MODE;
}
