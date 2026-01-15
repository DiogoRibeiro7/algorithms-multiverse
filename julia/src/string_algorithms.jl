"""
    StringAlgorithms

Module containing string algorithms implemented in Julia.
"""
module StringAlgorithms

export kmp_search, rabin_karp, boyer_moore, z_algorithm,
       longest_common_prefix, is_palindrome, all_palindromes,
       string_matching_wildcards, anagram_check, string_compression

"""
    kmp_search(text::String, pattern::String)

Search for pattern in text using KMP algorithm.
Time: O(n + m), Space: O(m)
"""
function kmp_search(text::String, pattern::String)
    m = length(pattern)
    n = length(text)

    if m == 0
        return Int[]
    end

    # Build LPS array
    lps = build_lps(pattern)
    matches = Int[]

    i = j = 1

    while i <= n
        if j <= m && text[i] == pattern[j]
            i += 1
            j += 1
        end

        if j > m
            push!(matches, i - j + 1)
            j = lps[m] + 1
        elseif i <= n && (j == 0 || text[i] != pattern[j])
            if j > 1
                j = lps[j - 1] + 1
            else
                i += 1
            end
        end
    end

    return matches
end

function build_lps(pattern::String)
    m = length(pattern)
    lps = zeros(Int, m)
    len = 0
    i = 2

    while i <= m
        if pattern[i] == pattern[len + 1]
            len += 1
            lps[i] = len
            i += 1
        else
            if len > 0
                len = lps[len]
            else
                lps[i] = 0
                i += 1
            end
        end
    end

    return lps
end

"""
    rabin_karp(text::String, pattern::String, prime::Int=101)

Search using Rabin-Karp rolling hash algorithm.
Time: O(n + m) average, Space: O(1)
"""
function rabin_karp(text::String, pattern::String, prime::Int=101)
    m = length(pattern)
    n = length(text)
    d = 256  # Number of characters in alphabet
    h = 1
    pattern_hash = 0
    text_hash = 0
    matches = Int[]

    # Calculate h = d^(m-1) % prime
    for _ in 1:m-1
        h = (h * d) % prime
    end

    # Calculate hash value of pattern and first window
    for i in 1:m
        pattern_hash = (d * pattern_hash + Int(pattern[i])) % prime
        text_hash = (d * text_hash + Int(text[i])) % prime
    end

    # Slide pattern over text
    for i in 1:n-m+1
        if pattern_hash == text_hash
            # Check characters one by one
            if text[i:i+m-1] == pattern
                push!(matches, i)
            end
        end

        # Calculate hash for next window
        if i < n - m + 1
            text_hash = (d * (text_hash - Int(text[i]) * h) + Int(text[i + m])) % prime
            if text_hash < 0
                text_hash += prime
            end
        end
    end

    return matches
end

"""
    z_algorithm(s::String)

Compute Z-array for string s.
Time: O(n), Space: O(n)
"""
function z_algorithm(s::String)
    n = length(s)
    z = zeros(Int, n)
    l = r = 0

    for i in 2:n
        if i > r
            l = r = i
            while r <= n && s[r - l + 1] == s[r]
                r += 1
            end
            z[i] = r - l
            r -= 1
        else
            k = i - l + 1
            if z[k] < r - i + 1
                z[i] = z[k]
            else
                l = i
                while r <= n && s[r - l + 1] == s[r]
                    r += 1
                end
                z[i] = r - l
                r -= 1
            end
        end
    end

    return z
end

"""
    longest_common_prefix(strs::Vector{String})

Find the longest common prefix of strings.
Time: O(S) where S is sum of all string lengths
"""
function longest_common_prefix(strs::Vector{String})
    if isempty(strs)
        return ""
    end

    prefix = strs[1]

    for i in 2:length(strs)
        while !startswith(strs[i], prefix)
            prefix = prefix[1:end-1]
            if isempty(prefix)
                return ""
            end
        end
    end

    return prefix
end

"""
    is_palindrome(s::String)

Check if string is a palindrome.
Time: O(n), Space: O(1)
"""
function is_palindrome(s::String)
    left = 1
    right = length(s)

    while left < right
        if s[left] != s[right]
            return false
        end
        left += 1
        right -= 1
    end

    return true
end

"""
    anagram_check(s1::String, s2::String)

Check if two strings are anagrams.
Time: O(n), Space: O(k) where k is alphabet size
"""
function anagram_check(s1::String, s2::String)
    if length(s1) != length(s2)
        return false
    end

    char_count = Dict{Char, Int}()

    for c in s1
        char_count[c] = get(char_count, c, 0) + 1
    end

    for c in s2
        if !haskey(char_count, c) || char_count[c] == 0
            return false
        end
        char_count[c] -= 1
    end

    return all(v == 0 for v in values(char_count))
end

"""
    string_compression(s::String)

Compress string using run-length encoding.
Time: O(n), Space: O(n)
"""
function string_compression(s::String)
    if isempty(s)
        return s
    end

    compressed = Char[]
    count = 1
    current = s[1]

    for i in 2:length(s)
        if s[i] == current
            count += 1
        else
            push!(compressed, current)
            if count > 1
                append!(compressed, string(count))
            end
            current = s[i]
            count = 1
        end
    end

    push!(compressed, current)
    if count > 1
        append!(compressed, string(count))
    end

    result = String(compressed)
    return length(result) < length(s) ? result : s
end

end # module StringAlgorithms