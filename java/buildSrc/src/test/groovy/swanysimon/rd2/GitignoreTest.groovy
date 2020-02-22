package swanysimon.rd2

import groovy.io.FileType
import groovy.transform.Memoized
import spock.lang.Specification
import spock.lang.Subject
import spock.lang.Unroll

class GitignoreTest extends Specification {

    private static List<File> gitignores = []

    def setupSpec() {
        def onDisk = new File(this.class.protectionDomain.codeSource.location.toURI())
        def projectRoot = "git -C ${onDisk.absolutePath} rev-parse --show-toplevel".execute().text.trim()
        new File(projectRoot).absoluteFile.eachFileRecurse(FileType.FILES) {
            if (it.name == ".gitignore" && !(it.absoluteFile in gitignores)) {
                gitignores << it.absoluteFile
            }
        }
    }

    def "there is at least one gitignore file"() {
        expect:
        !gitignores.isEmpty()
    }

    @Unroll
    def "gitignore files contain no empty lines"() {
        given:
        def contents = getContents(gitignore)
        def lines = contents.headerLines + contents.ignoreLines

        expect:
        lines.every { !it.isBlank() }

        where:
        gitignore << gitignores
    }

    @Unroll
    def "gitignore negations are at the end of the file"() {
        given:
        def lines = getContents(gitignore).ignoreLines

        expect:
        lines.last().startsWith("!") || !lines.every { it.startsWith("!") }

        where:
        gitignore << gitignores
    }

    @Unroll
    def "gitignore header follows the desired ordering"() {
        given:
        def lines = getContents(gitignore).headerLines

        expect:
        lines.size >= 2
        lines.first() == "# This gitignore file was generated from the following sources:"
        lines.last() == "# The contents were then sorted, reversed, and comments removed."

        when:
        def sourceLines = lines[1..lines.size - 2]

        then:
        sourceLines.toSorted().toUnique() == sourceLines
        sourceLines.every { it ==~ '^#   - [A-Z]\\S*: http\\S+$' }

        where:
        gitignore << gitignores
    }

    @Unroll
    def "gitignore ignorefollows the desired ordering"() {
        given:
        def lines = getContents(gitignore).ignoreLines

        expect:
        lines.every { !it.startsWith("#") }
        lines.toSorted { a, b -> b.compareTo(a) }.toUnique() == lines

        where:
        gitignore << gitignores
    }

    @Unroll
    def "gitignore contents are fully populated by sources in header"() {
        given:
        def contents = getContents(gitignore)
        def sources = contents.headerLines
                .findAll { it.contains("http") }
                .collect { it.split(":", 2)[1].trim() }

        when:
        def sourceText = sources.collect { getLines(it) }
                .flatten()
                .toSorted { a, b -> b.compareTo(a) }
                .toUnique()

        then:
        sourceText == contents.ignoreLines

        where:
        gitignore << gitignores
    }

    @Memoized
    private static GitignoreContents getContents(File gitignore) {
        def contents = new GitignoreContents()
        def lines = gitignore.readLines()
        lines.takeWhile { it.startsWith("#") }.each { contents.headerLines << it }
        lines.dropWhile { it.startsWith("#") }.each { contents.ignoreLines << it }
        return contents
    }

    @Memoized
    private static List<String> getLines(String url) {
        return url.toURL().text.lines().findAll { !it.startsWith("#") && !it.isBlank() }
    }

    private static final class GitignoreContents {
        private final List<String> headerLines = []
        private final List<String> ignoreLines = []
    }
}
