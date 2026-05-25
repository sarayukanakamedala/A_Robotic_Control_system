import { createClient } from '@supabase/supabase-js'

const supabaseUrl = "https://iqsiieniwodtqaefbhzy.supabase.co"
const supabaseKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlxc2lpZW5pd29kdHFhZWZiaHp5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzMzMTQwNjAsImV4cCI6MjA4ODg5MDA2MH0.HHDXHMenlfF0-bvLhn6sGUzZtGea4VgX4AL7edRpPxI"

export const supabase = createClient(supabaseUrl, supabaseKey)